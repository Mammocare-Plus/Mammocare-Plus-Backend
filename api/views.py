from users.models import MCPUser
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
from api.serializers import (
    ClinicSerializer,
    DoctorSerializer,
    DiseaseSerializer,
    HistorySerializer,
    PatientSerializer,
    CaseSerializer,
    RecordSerializer,
    ChatSerializer,
    MessageSerializer,
    NotificationSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class ClinicViewSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    pagination_class = PageNumberPagination
    
    def list(self, request):
        user = request.user
        if user.is_admin:
            clinics = Clinic.objects.all()
            serializer = ClinicSerializer(clinics, many=True)
            return Response(serializer.data)
        else:
            clinics = Clinic.objects.filter(isActive=True)
            serializer = ClinicSerializer(clinics, many=True)
            return Response(serializer.data)
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            clinic = Clinic.objects.get(id=pk)
            serializer = ClinicSerializer(clinic)
            return Response(serializer.data)
        else:
            clinic = Clinic.objects.get(id=pk, isActive=True)
            serializer = ClinicSerializer(clinic, many=True)
            return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin or user.isDoctor:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a clinic"}, status=403)
    
    def update(self, request, pk):
        user = request.user
        if user.isDoctor and user.is_active:
            doctor = Doctor.objects.get(user=user)
            clinic = Clinic.objects.get(id=pk, doctor=doctor)
            if clinic:
                serializer = ClinicSerializer(clinic, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        elif user.is_admin:
            clinic = Clinic.objects.get(id=pk)
            if clinic:
                serializer = ClinicSerializer(clinic, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        else:
            return Response({"message": "You are not allowed to update a clinic"}, status=403)
                
    def destroy(self, request, pk):
        user = request.user
        if user.isDoctor and user.is_active:
            doctor = Doctor.objects.get(user=user)
            clinic = Clinic.objects.get(id=pk, doctor=doctor)
            if clinic:
                clinic.isActive = False
                clinic.save()
                return Response({"message": "Clinic deleted successfully"})
            else:
                return Response({"message": "Clinic not found"}, status=404)
        elif user.is_admin:
            clinic = Clinic.objects.get(id=pk)
            if clinic:
                clinic.isActive = False
                clinic.save()
                return Response({"message": "Clinic deleted successfully"})
            else:
                return Response({"message": "Clinic not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a clinic"}, status=403)
        

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = PageNumberPagination
    
    def list(self, request):
        user = request.user
        if user.is_admin:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
        else:
            doctors = Doctor.objects.filter(isActive=True)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            doctor = Doctor.objects.get(id=pk)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        else:
            doctor = Doctor.objects.get(id=pk, isActive=True)
            serializer = DoctorSerializer(doctor, many=True)
            return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a doctor"}, status=403)
    
    def update(self, request, pk):
        user = request.user
        if user.isDoctor and user.is_active:
            doctor = Doctor.objects.get(user=user)
            if doctor:
                serializer = DoctorSerializer(doctor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        elif user.is_admin:
            doctor = Doctor.objects.get(id=pk)
            if doctor:
                serializer = DoctorSerializer(doctor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        else:
            return Response({"message": "You are not allowed to update a doctor"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.isDoctor:
            doctor = Doctor.objects.get(id=pk, user=user)
            if doctor:
                doctor.isActive = False
                doctor.save()
                return Response({"message": "Doctor deleted successfully"})
            else:
                return Response({"message": "Doctor not found"}, status=404)
        elif user.is_admin:
            doctor = Doctor.objects.get(id=pk)
            if doctor:
                doctor.isActive = False
                doctor.save()
                return Response({"message": "Doctor deleted successfully"})
            else:
                return Response({"message": "Doctor not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a doctor"}, status=403)

class DiseaseViewSet(ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            disease = Disease.objects.all()
            serializer = DiseaseSerializer(disease, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Not allowed to view diseases"})
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_active:
            disease = Disease.objects.get(id=pk)
            serializer = DiseaseSerializer(disease)
            return Response(serializer.data)
        else:
            return Response({"message": "Not allowed to view diseases"})
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a disease"}, status=403)
    
class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            history = History.objects.all()
            serializer = HistorySerializer(history, many=True)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(user=user)
            history = History.objects.filter(patient=patient)
            serializer = HistorySerializer(history, many=True)
            return Response(serializer.data)

    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            history = History.objects.get(id=pk)
            serializer = HistorySerializer(history)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(user=user)
            history = History.objects.get(id=pk, patient=patient, isActive = True)
            serializer = HistorySerializer(history, many=True)
            return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a history"}, status=403)
    
    def update(self, request, pk):
        user = request.user
        if user.is_active and user.isDoctor == False:
            patient = Patient.objects.get(user=user)
            history = History.objects.get(patient=patient, id=pk)
            if history:
                serializer = HistorySerializer(history, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        elif user.is_admin:
            history = History.objects.get(id=pk)
            if history:
                serializer = HistorySerializer(history, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        else:
            return Response({"message": "You are not allowed to update a history"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.is_active and user.isDoctor == False:
            patient = Patient.objects.get(user=user)
            history = History.objects.get(id=pk, patient=patient)
            if history:
                history.isActive = False
                history.save()
                return Response({"message": "History deleted successfully"})
            else:
                return Response({"message": "History not found"}, status=404)
        elif user.is_admin:
            history = History.objects.get(id=pk)
            if history:
                history.isActive = False
                history.save()
                return Response({"message": "History deleted successfully"})
            else:
                return Response({"message": "History not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a history"}, status=403)

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            patient = Patient.objects.all()
            serializer = PatientSerializer(patient, many=True)
            return Response(serializer.data)
        else:
            patient = Patient.objects.filter(isActive=True)
            serializer = PatientSerializer(patient, many=True)
            return Response(serializer.data)
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            patient = Patient.objects.get(id=pk)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(id=pk, isActive=True)
            serializer = PatientSerializer(patient, many=True)
            return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user = MCPUser.objects.get(id=user_id)
        if user.is_active:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a patient"}, status=403)
    
    def update(self, request, pk):
        user = request.user
        if user.isDoctor == False and user.is_active:
            patient = Patient.objects.get(user=user)
            if patient:
                serializer = PatientSerializer(patient, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        elif user.is_admin:
            patient = Patient.objects.get(id=pk)
            if patient:
                serializer = PatientSerializer(patient, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
        else:
            return Response({"message": "You are not allowed to update a patient"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.isDoctor == False:
            patient = Patient.objects.get(id=pk, user=user)
            if patient:
                patient.isActive = False
                patient.save()
                return Response({"message": "Patient deleted successfully"})
            else:
                return Response({"message": "Patient not found"}, status=404)
        elif user.is_admin:
            patient = Patient.objects.get(id=pk)
            if patient:
                patient.isActive = False
                patient.save()
                return Response({"message": "Patient deleted successfully"})
            else:
                return Response({"message": "Patient not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a Patient"}, status=403)

class CaseViewSet(ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            cases = Case.objects.all()
            serializer = CaseSerializer(cases, many=True)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(user=user)
            doctor = Doctor.objects.get(user=user)
            if patient:
                cases = Case.objects.filter(patient=patient, isActive=True)
                serializer = CaseSerializer(cases, many=True)
                return Response(serializer.data)
            elif doctor:
                cases = Case.objects.filter(doctor=doctor, isActive=True)
                serializer = CaseSerializer(cases, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Not allowed to view cases"})
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            case = Case.objects.get(id=pk)
            serializer = CaseSerializer(patient)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(user=user)
            doctor = Doctor.objects.get(user=user)
            if patient:
                case = Case.objects.get(id=pk, patient=patient, isActive=True)
                serializer = CaseSerializer(case)
                return Response(serializer.data)
            elif doctor:
                case = Case.objects.get(id=pk, doctor=doctor, isActive=True)
                serializer = CaseSerializer(case)
                return Response(serializer.data)
            else:
                return Response({"message": "Not allowed to view cases"})
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if (user.isDoctor and user.is_active) or user.is_admin:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a case"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.isDoctor and user.is_active:
            doctor = Doctor.objects.get(user=user)
            case = Case.objects.get(id=pk, doctor=doctor)
            if case:
                case.isActive = False
                case.save()
                return Response({"message": "Case deleted successfully"})
            else:
                return Response({"message": "Case not found"}, status=404)
        elif user.is_admin:
            case = Case.objects.get(id=pk)
            if case:
                case.isActive = False
                case.save()
                return Response({"message": "Case deleted successfully"})
            else:
                return Response({"message": "Case not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a case"}, status=403)

class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        print(user)
        if user.is_admin:
            records = Record.objects.all()
            serializer = RecordSerializer(records, many=True)
            return Response(serializer.data)
        elif user.isDoctor == False:
            patient = Patient.objects.get(user=user)
            records = Record.objects.filter(patient=patient, isActive=True)
            serializer = RecordSerializer(records, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Not allowed to view records"})
    
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            record = Record.objects.get(id=pk)
            serializer = RecordSerializer(record)
            return Response(serializer.data)
        else:
            patient = Patient.objects.get(user=user)
            record = Record.objects.get(id=pk, patient=patient, isActive=True)
            serializer = RecordSerializer(record)
            return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_active and user.isDoctor == False:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to create a record"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.is_active and user.isDoctor == False:
            patient = Patient.objects.get(user=user)
            record = Record.objects.get(id=pk, patient=patient)
            if record:
                record.isActive = False
                record.save()
                return Response({"message": "Record deleted successfully"})
            else:
                return Response({"message": "Record not found"}, status=404)
        elif user.is_admin:
            record = Record.objects.get(id=pk)
            if record:
                record.isActive = False
                record.save()
                return Response({"message": "Record deleted successfully"})
            else:
                return Response({"message": "Record not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a record"}, status=403)

class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            chats = Chat.objects.all()
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data)
        else:
            chats = Chat.objects.filter(Q(doctor=user) | Q(patient=user)).filter(isActive=True)
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data)
        
    def retrieve(self, request, pk):
        """
        This function is used to retrieve a chat between two users.
        One user will be the current user and the other user will be the user with the pk passed in the url.
        NOTE: pk is the pk of the other user in the chat.
        """
        user = request.user
        if user.is_admin:
            chat = Chat.objects.get(Q(doctor__id=pk) | Q(patient__id=pk), isActive=True)
            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
            else:
                return Response({"message": "Chat not found"}, status=404)
        if user.isDoctor and user.is_active:
            patient = Patient.objects.get(id=pk)
            chat = Chat.objects.filter(isActive=True).get(Q(doctor=user) | Q(patient=patient))
            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
            else:
                return Response({"message": "Chat not found"}, status=404)
        elif user.isDoctor == False and user.is_active:
            doctor = Doctor.objects.get(id=pk)
            chat = Chat.objects.filter(isActive=True).get(Q(doctor=doctor) | Q(patient=user))
            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
            else:
                return Response({"message": "Chat not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to view a chat"}, status=403)
            
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return super().create(request, *args, **kwargs)
        else:
            chatData = request.data
            if user.isDoctor and user.is_active:
                chatData['doctor'] = user.id
                serializer = ChatSerializer(data=chatData)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            elif user.isDoctor == False and user.is_active:
                chatData['patient'] = user.id
                serializer = ChatSerializer(data=chatData)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response({"message": "You are not allowed to create a chat"}, status=403)
            
    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to update a chat"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.is_admin:
            chat = Chat.objects.get(id=pk)
            if chat:
                chat.isActive = False
                chat.save()
                return Response({"message": "Chat deleted successfully"})
            else:
                return Response({"message": "Chat not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a chat"}, status=403)

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        if user.is_admin:
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        else:
            messages = Message.objects.filter(Q(chat__doctor=user) | Q(chat__patient=user)).filter(isActive=True)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """
        This function is used to retrieve all the messages in a chat.
        NOTE: pk is the pk of the chat. NOT the message.
        """
        user = request.user
        if user.is_admin:
            message = Message.objects.filter(chat__id=pk)
            serializer = MessageSerializer(message, many=True)
            return Response(serializer.data)
        else:
            messages = Message.objects.filter(Q(chat__doctor=user) | Q(chat__patient=user)).filter(chat__id=pk, isActive=True)
            if messages:
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Messages not found"}, status=404)
            
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return super().create(request, *args, **kwargs)
        else:
            messageData = request.data
            chat = Chat.objects.get(id=messageData['chat'])
            if chat:
                if chat.doctor == user or chat.patient == user:
                    serializer = MessageSerializer(data=messageData)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=400)
                else:
                    return Response({"message": "You are not allowed to send a message in this chat"}, status=403)
            else:
                return Response({"message": "Chat not found"}, status=404)
            
    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to update a message"}, status=403)
        
    def destroy(self, request, pk):
        user = request.user
        if user.is_admin:
            message = Message.objects.get(id=pk)
            if message:
                message.isActive = False
                message.save()
                return Response({"message": "Message deleted successfully"})
            else:
                return Response({"message": "Message not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a message"}, status=403)
        
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            notifications = Notification.objects.all(user=user)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        else:
            notifications = Notification.objects.filter(user=user, isActive=True)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        
    def retrieve(self, request, pk):
        user = request.user
        if user.is_admin:
            notification = Notification.objects.get(id=pk)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
        else:
            notification = Notification.objects.get(id=pk, user=user, isActive=True)
            if notification:
                serializer = NotificationSerializer(notification)
                return Response(serializer.data)
            else:
                return Response({"message": "Notification not found"}, status=404)
            
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.isActive:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"message": "You are not allowed to update a notification"}, status=403)    
    
    def destroy(self, request, pk):
        user = request.user
        if user.isActive:
            notification = Notification.objects.get(id=pk, user=user)
            if notification:
                notification.isActive = False
                notification.save()
                return Response({"message": "Notification deleted successfully"})
            else:
                return Response({"message": "Notification not found"}, status=404)
        else:
            return Response({"message": "You are not allowed to delete a notification"}, status=403)