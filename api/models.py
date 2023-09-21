from django.db import models
import uuid 
from users.models import MCPUser
from phonenumber_field.modelfields import PhoneNumberField

class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = PhoneNumberField(unique=True, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.OneToOneField(MCPUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    yoe = models.IntegerField(null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctor')
    isActive = models.BooleanField(default=True)
    charge = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username

class Disease(models.Model):
    DISEASE_CHOICES = (
        ('Eczema', 'Eczema'),
        ('Warts Molluscum and other Viral Infection', 'Warts Molluscum and other Viral Infection'),
        ('Melanoma', 'Melanoma'),
        ('Atopic Dermatatis', 'Atopic Dermatatis'),
        ('Basal Cell Carcinoma', 'Basal Cell Carcinoma'),
        ('Melanocytic Nevi (NV)', 'Melanocytic Nevi (NV)'),
        ('Benign Keratosis-like Lesions (BKL)', 'Benign Keratosis-like Lesions (BKL)'),
        ('Psoriasis pictures Lichen Planus and related diseases', 'Psoriasis pictures Lichen Planus and related diseases'),
        ('Seborrheic Keratoses and other Benign Tumors', 'Seborrheic Keratoses and other Benign Tumors'),
        ('Tinea Ringworm Candidiasis and other Fungal Infections', 'Tinea Ringworm Candidiasis and other Fungal Infections')
    )
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, choices=DISEASE_CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    hindi_name = models.CharField(max_length=255, choices=DISEASE_CHOICES, null=True, blank=True)
    hindi_description = models.TextField(null=True, blank=True)
    hindi_prescription = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.name

class History(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='history')
    affected = models.JSONField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.disease.name

class Patient(models.Model):
    
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.OneToOneField(MCPUser, on_delete=models.CASCADE, related_name='patient')
    history = models.OneToOneField(History, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient')
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username

class Case(models.Model):
    REQUEST_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='case')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='case')
    requestDescription = models.TextField(null=True, blank=True)
    record = models.OneToOneField('Record', on_delete=models.SET_NULL, null=True, blank=True, related_name='case')
    requestStatus = models.CharField(max_length=100, choices=REQUEST_STATUS_CHOICES, default='Pending', null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.doctor.user.username

class Record(models.Model):
    LOCALISATION_CHOICES = (
        ('Face', 'Face'),
        ('Scalp', 'Scalp'),
        ('Hands', 'Hands'),
        ('Feet', 'Feet'),
        ('Arms and Legs', 'Arms and Legs'),
        ('Chest and Back', 'Chest and Back'),
        ('Groin', 'Groin'),
        ('Nails', 'Nails'),
        ('Mouth and Lips', 'Mouth and Lips'),
        ('Underarms', 'Underarms'),
        ('Palms and Soles', 'Palms and Soles'),
        ('Ears', 'Ears'),
        ('Back of the Neck', 'Back of the Neck'),
    )

    MODEL_CHOICES = (
        ('efficientnetb2', 'efficientnetb2'),
        ('efficientnetb4', 'efficientnetb4'),
        ('efficientnetb7', 'efficientnetb7'),
        ('mobilenetv2', 'mobilenetv2')
    )
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='record')
    model = models.CharField(max_length=15, choices=MODEL_CHOICES, null=True, blank=True, default= MODEL_CHOICES[2])
    prediction = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='record')
    uploadedImage = models.URLField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(choices= LOCALISATION_CHOICES, null=True, blank= True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.patient.user.username} -- {self.prediction.name}"

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='chat')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chat')
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.doctor.user.username} -- {self.patient.user.username}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    body = models.TextField(null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='message')
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.body[:50]}..."
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(MCPUser, on_delete=models.CASCADE, related_name='notification')
    title = models.CharField(max_length=255, null=False, blank=True)
    body = models.TextField(null=True, blank=True)
    redirectUrl = models.URLField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isread = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} -- {self.body[:50]}..."