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
from rest_framework.serializers import ModelSerializer, IntegerField, UUIDField
from users.models import MCPUser

class ClinicSerializer(ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phoneNumber', 'city', 'state', 'area', 'isActive']

class DoctorSerializer(ModelSerializer):
    clinic = ClinicSerializer()
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'qualification', 'university', 'yoe', 'clinic', 'isActive', 'charge']
    
    def create(self, validated_data):
        clinic_data = validated_data.pop('clinic')
        clinic = Clinic.objects.create(**clinic_data)
        doctor = Doctor.objects.create(clinic=clinic, **validated_data)
        return doctor

class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'prescription', 'symptoms', 'isActive', 'hindi_name', 'hindi_description', 'hindi_prescription']

class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'disease', 'affected', 'createdAt', 'updatedAt', 'isActive']

class PatientSerializer(ModelSerializer):
    user_id = UUIDField(write_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'history', 'isActive', 'user_id']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = MCPUser.objects.get(id=user_id)
        validated_data['user'] = user
        patient = Patient.objects.create(**validated_data)
        return patient
    
class CaseSerializer(ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'patient', 'doctor', 'requestDescription', 'record', 'requestStatus', 'createdAt', 'updatedAt', 'isActive']

class RecordSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'patient', 'model', 'prediction', 'uploadedImage', 'createdAt', 'localisation', 'isActive']

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'doctor', 'patient', 'createdAt', 'isActive']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'body', 'chat', 'createdAt', 'isActive']

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'body', 'redirectUrl', 'createdAt', 'isread', 'isActive']