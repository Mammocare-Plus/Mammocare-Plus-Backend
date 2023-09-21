from django.contrib import admin
from api.models import Patient, Doctor, Clinic, Disease, History, Case, Record, Chat, Message, Notification

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Disease)
admin.site.register(History)
admin.site.register(Case)
admin.site.register(Record)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Notification)