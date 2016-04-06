from django.contrib import admin

# Register your models here.
from .models import ElegibilityCertificate, Candidate, CandidateInCertificate, ContactInfo, ContactAttempt, \
    CertificateResult, Interview


class CandidateInCertificateInLine(admin.TabularInline):
    model = CandidateInCertificate


class ElegibilityCertificateAdmin(admin.ModelAdmin):
    list_display = ('number', 'grade', 'vacant_positions', 'expires', 'date_closed')
    inlines = (CandidateInCertificateInLine, )

class CandidateInCertificateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'certificate', 'certificate_result', 'candidate', 'score', 'explanation')
    list_editable = ( 'certificate_result', 'candidate', 'score', 'explanation')
    list_filter = ('certificate', )


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'candidate', 'number', 'email', 'instructions', 'comments', 'valid')

class ContactInfoInLine(admin.TabularInline):
    model = ContactInfo

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'national_id')
    ordering = ('last_name', 'first_name')
    inlines = (ContactInfoInLine,)

class ContactAttemptAdmin(admin.ModelAdmin):
    list_display = ('contact_method', 'candidate_certificate', 'succesful_contact', 'contact_datetime', 'comments')


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate_certificate', 'start_datetime', 'end_datetime', 'comments')


admin.site.register(ElegibilityCertificate, ElegibilityCertificateAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateInCertificate, CandidateInCertificateAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(ContactAttempt, ContactAttemptAdmin)
admin.site.register(CertificateResult)
admin.site.register(Interview, InterviewAdmin)