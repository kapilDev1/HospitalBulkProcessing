import requests
from time import sleep


BASE_URL = "https://hospital-directory.onrender.com"


class HospitalDirectoryClient():

    def create_hospital(self,payload, retries=1):
        url = f"{BASE_URL}/hospitals/"
        for attempt in range(retries+1):
            try:
                response = requests.post(url=url,json=payload, timeout=30)
                return response
            except requests.RequestException:
                if attempt==retries:
                    raise
                sleep(0.5)
    
    def activate_batch(self,batch_id):
        url = f"{BASE_URL}/hospitals/batch/{batch_id}/activate"
        response = requests.patch(url=url,timeout=30)
        return response