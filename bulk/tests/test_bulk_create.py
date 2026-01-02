from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from unittest.mock import patch,MagicMock

client = APIClient()

def make_csv():
    return SimpleUploadedFile(
        "hospitals.csv",
        b"name,address\nHospital A,Addr A\n",
        content_type="text/csv"
    )

@patch("bulk.views.HospitalDirectoryClient")
def test_bulk_create_success(mock_client):
    mock_instance = mock_client.return_value

    mock_create = MagicMock()
    mock_create.status_code = 200
    mock_create.json.return_value = {"id":123}
    
    mock_activate = MagicMock()
    mock_activate.status_code = 200

    mock_instance.create_hospital.return_value = mock_create
    mock_instance.activate_batch.return_value = mock_activate

    response = client.post(
        "/hospitals/bulk",
        {"file":make_csv()},
        format="multipart"
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["batch_activated"] is True
    assert data["failed_hospitals"]==0