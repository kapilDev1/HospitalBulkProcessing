#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid
import time

from .utils import validate_and_parse_csv
from .services.hospital_client import HospitalDirectoryClient

# Create your views here.

class CSVValidateView(APIView):

    def post(self,request):
        file = request.FILES.get('file')

        if not file:
            return Response({"valid":False, "error":"CSV file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rows = validate_and_parse_csv(file)
        
        except ValueError as e:
            return Response(
                {"valid": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "valid": True,
            "total_hospitals": len(rows),
            "preview": rows[:2]  
        })


class BulkHospitalCreateView(APIView):
    
    def post(self,request):
        start_time = time.time()
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "CSV file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            hospitals = validate_and_parse_csv(file)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        
        batch_id = str(uuid.uuid4())
        client = HospitalDirectoryClient()

        results = []
        failed = 0

        for idx,hospital in enumerate(hospitals,start=1):
            payload = {
                "name":hospital["name"],
                "address":hospital["address"],
                "phone":hospital["phone"],
                "creation_batch_id":batch_id,
            }

            try:
                response = client.create_hospital(payload)
                #print(response)
                #print(response.text)
            except Exception as e:
                failed+=1
                results.append({
                    "row":idx,
                    "name":hospital["name"],
                    "status":"failed",
                    "error":str(e)
                })
                continue

            if response.status_code in (200,201):
                results.append({
                    "row":idx,
                    "hospital_id":response.json().get("id"),
                    "name":hospital["name"],
                    "status":"created" 
                })
            else:
                failed+=1
                results.append({
                    "row":idx,
                    "name":hospital["name"],
                    "status":"failed",
                    "error":response.text
                })

        batch_activated = False

        if failed==0:
            try:
                activation_response = client.activate_batch(batch_id)
                if activation_response.status_code in (200,204):
                    batch_activated = True
                    for r in results:
                        r['status']="created_and_activated"
                else:
                    for r in results:
                        r['status']="created_but_activation_failed"
            except Exception as e:
                for r in results:
                    r['status']="created_but_activation_failed"


        return Response({
                "batch_id":batch_id,
                "total_hospitals":len(hospitals),
                "processed_hospitals":len(hospitals)-failed,
                "failed_hospitals":failed,
                "processing_time_seconds":int(time.time()-start_time),
                "batch_activated":batch_activated,
                "hospitals":results
        },status=status.HTTP_201_CREATED)