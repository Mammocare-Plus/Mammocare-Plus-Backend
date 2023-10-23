from users.models import (
    MCPUser
)
from api.models import (
    Clinic,
    Doctor,
    Disease,
    History,
    Patient,
    Case,
    Record,
    Chat,
    Message,
    Notification
)
from users.serializers import (
    MCPUserSerializer
)
from api.serializers import (
    ClinicSerializer,
    DoctorSerializer,
    DiseaseSerializer,
    HistorySerializer,
    PatientSerializer,
    CaseSerializer,
    RecordSerializer,
    ChatSerializer,
    MessageSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import api.utils as utils

# TODO: Create custom APIs here

class CheckDoctor(APIView):
    def get(self, request):
        user = request.user
        if user.isDoctor:
            return Response({"isDoctor": True}, status=status.HTTP_200_OK)
        else:
            return Response({"isDoctor": False}, status=status.HTTP_200_OK)

class AddToHistory(APIView):
    def post(self, request):
        try:
            record = Record.objects.get(id=request.data['record'])
            patient = record.patient
            disease = record.prediction
            name = patient.user.username 
            age = patient.user.age  
            affected_dict = {
                "name" : name,
                "age" : age
            }
            affected_json = json.dumps(affected_dict)
            History.objects.create(
                disease=disease,
                affected=affected_json
            )
            return Response({"message": "Added to history"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
class CountOfPatientRecords(APIView):
    def get(self, request):
        try:
            user = request.user
            patient = Patient.objects.get(user=user)
            records = Record.objects.filter(patient=patient)
            count = len(records)
            return Response({"count": count}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        

class CasesHandled(APIView):
    def post(self, request, pk):
        user:MCPUser = request.user
        if user.isDoctor:
            cases = Case.objects.filter(doctor = user, isActive=True, REQUEST_STATUS_CHOICES='Accepted')
            
            return Response({"Case Count": len(cases)}, status=status.HTTP_200_OK)
        else:
            return Response({"isDoctor": False}, status=status.HTTP_200_OK)
        

class ClinicLocations(APIView):
    def post(self, request, pk):
        user:MCPUser = request.user
        if user.isDoctor:
            doctor = Doctor.objects.filter(id=pk)
            clinics = doctor[0].clinic
            ans=[]
            for i in clinics:
                ans.append(utils.get_coordinates(i))
            
            return Response({"Clinic Locations": ans}, status=status.HTTP_200_OK)


class GetNearestClinic(APIView):
    def get(self, request):
        user:MCPUser = request.user
        doctors = Doctor.objects.all()
        min, doc, cli = utils.GetNearestClinic(user.address, doctors)
        return Response({"Nearest Doctor": doc, "Nearest Clinic": cli}, status=status.HTTP_200_OK)
    
class ConnectToDoctor(APIView):
    def post(self, request):
        user = request.user
        doctor = Doctor.objects.get(id=request.data['doctor'])
        record = Record.objects.get(id=request.data['record'])
        case = Case.objects.create(
            patient=user.patient,
            doctor = doctor,
            requestDescription=request.data['requestDescription'],
            record=record,
            requestStatus='Pending'
        )
        Notification.objects.create(
            user=doctor.user,
            title='New Case',
            body=f'You have a new case from {user.username}'
        )
        serializer=CaseSerializer(case)
        return Response({"message": "Case created", "data": serializer.data}, status=status.HTTP_200_OK)


class DiagnosisReport(APIView):
    def post(self, request, pk):
        diagnosis = Record.objects.get(id=pk)
        patient = diagnosis.patient.user
        doctors = Doctor.objects.all()
        min, doc, cli = utils.GetNearestClinic(patient.address, doctors)
        return Response({"Diagnosis": diagnosis, "Nearest Doctor": doc, "Nearest Clinic": cli}, status=status.HTTP_200_OK)

class RecordAfterInference(APIView):
    def post(self, request):
        try:
            print(request.data)
            user = request.user
            patient = Patient.objects.get(user=user)
            model = request.data['model']
            prediction = request.data['prediction']
            diseases = utils.get_diseases()
            # print(diseases)
            diseases_json = diseases['diseases']
            disease = None
            for i in diseases_json:
                if i['name'] == prediction:
                    disease = i 
                    break
            disease_obj = Disease.objects.create(
                name=disease['name'],
                description=disease['description'],
                prescription=disease['prescription'],
                symptoms=disease['symptoms'],
                isActive=disease['isActive'],
                hindi_name=disease['hindi_name'],
                hindi_description=disease['hindi_description'],
                hindi_prescription=disease['hindi_prescription']
            )
            uploadedImage = request.data['uploadedImage']
            record = Record.objects.create(
                patient=patient,
                model=model,
                prediction=disease_obj,
                uploadedImage=uploadedImage
            )
            return Response({"message": "Record created", "data": record.id}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    