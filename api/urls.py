from api.views import (
    ClinicViewSet,
    DoctorViewSet,
    DiseaseViewSet,
    HistoryViewSet,
    PatientViewSet,
    RecordViewSet,
    ChatViewSet,
    MessageViewSet
)
from api.apis import (
    CheckDoctor,
    AddToHistory,
    CountOfPatientRecords,
    CasesHandled,
    ClinicLocations,
    GetNearestClinic,
    ConnectToDoctor,
    DiagnosisReport,
    RecordAfterInference
)
from rest_framework.routers import SimpleRouter
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response

router = SimpleRouter()
router.register(r'clinic', ClinicViewSet, basename='clinic')
router.register(r'doctor', DoctorViewSet, basename='doctor')
router.register(r'disease', DiseaseViewSet, basename='disease')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'patient', PatientViewSet, basename='patient')
router.register(r'record', RecordViewSet, basename='record')
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'message', MessageViewSet, basename='message')

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to MCP API',
            'endpoints': [
                '/clinic/',
                '/doctor/',
                '/disease/',
                '/history/',
                '/patient/',
                '/record/',
                '/chat/',
                '/message/',
            ]
        })
    
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('check-doctor/', CheckDoctor.as_view(), name="check-doctor"),
    path('add-to-history/', AddToHistory.as_view(), name="add-to-history"),
    path('count-of-patient-records/', CountOfPatientRecords.as_view(), name="count-of-patient-records"),
    path('cases-handled/', CasesHandled.as_view(), name='cases-handled'),
    path('clinic-locations/', ClinicLocations.as_view(), name='clinic-locations'),
    path('get-nearest-clinic/', GetNearestClinic.as_view(), name='get_nearest-clinic'),
    path('connect-to-doctor/', ConnectToDoctor.as_view(), name='connect-to-doctor'),
    path('diagnosis-report/', DiagnosisReport.as_view(), name='diagnosis-report'),
    path('record-after-inference/', RecordAfterInference.as_view(), name='record-after-inference'),
] + router.urls