import requests
from geopy.distance import geodesic
import boto3
import os
from dotenv import load_dotenv  
load_dotenv()
import json

def get_coordinates(address):
        try:
            response = requests.get(
                f'https://nominatim.openstreetmap.org/search?format=json&q={address}'
            )
            data = response.json()

            if response.status_code == 200 and data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)

            return None
        except Exception as e:
            return None

def calculate_distance(coordinates1, coordinates2):
    return geodesic(coordinates1, coordinates2).kilometers

# for doctor in doctors:
#     cords = get_coordinates(doctor.address)
#     dist = calculate_distance(cord1, cords)
#     if dist<min:
#         min = dist
#         doc=doctor

# return doc 

def GetNearestClinic(patientAddress, doctors):
    patientCors = get_coordinates(patientAddress)
    doc = ""
    cli = ""
    min = float('inf')
    for doctor in doctors:
        clinic = doctor.clinic
        doctorCors = get_coordinates(clinic.address)
        dist = calculate_distance(coordinates1=doctorCors, coordinates2=patientCors)
        if dist<min:
            min = dist
            doc = doctor
            cli = clinic
    
    return (min, doc, cli)
def upload_data(folder_path: str, remote_path: str) -> bool:
    try:
        s3 = boto3.resource('s3', region_name=os.getenv("REGION"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
        fileName = folder_path.split('/')[-1]
        remote_path = os.path.join(remote_path, fileName)
        s3.meta.client.upload_file(folder_path, os.getenv("S3_BUCKET"), remote_path)
        return True
    except Exception as e:
        return e
    
def get_diseases():
    with open(r'C:\Users\athar\OneDrive\Desktop\coding\projects\Mammocare Plus\backend\api\diseases.json', encoding='utf-8') as f:
        disease_data = json.load(f)

    return disease_data

if __name__ == '__main__':
    print(get_diseases())