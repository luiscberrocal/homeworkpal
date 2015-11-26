from django.contrib import admin

# Register your models here.
from .models import ElegibilityCertificate, Candidate, CandidateInCertificate, ContactInfo, ContactAttempt, \
    CertificateResult


class ElegibilityCertificateAdmin(admin.ModelAdmin):
    pass

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'national_id')

class CandidateInCertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate', 'score', 'candidate')

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'number', 'email', 'instructions', 'comments', 'valid')

class ContactAttemptAdmin(admin.ModelAdmin):
    list_display = ('contact_method', 'succesful_contact', 'contact_datetime', 'comments')

admin.site.register(ElegibilityCertificate, ElegibilityCertificateAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateInCertificate, CandidateInCertificateAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(ContactAttempt, ContactAttemptAdmin)
admin.site.register(CertificateResult)