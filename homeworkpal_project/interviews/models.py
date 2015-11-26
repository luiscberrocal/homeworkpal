from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel
from employee.models import Employee


class ElegibilityCertificate(TimeStampedModel):
    number = models.CharField(max_length=100)
    grade = models.CharField(max_length=5)
    ends_at = models.DateField()
    vacant_positions = models.PositiveIntegerField(default=1)
    emitted = models.DateField()
    expires = models.DateField()
    salary_per_year = models.DecimalField(max_digits=8, decimal_places=2)

    def monthly_salary(self):
        return self.salary_per_year/12.0

    def __str__(self):
        return self.number


class Candidate(TimeStampedModel):
    national_id = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class CertificateResult(TimeStampedModel):
    action = models.CharField(max_length=3)
    description = models.TextField()
    observations = models.TextField(blank=True)

    def __str__(self):
        return self.action


class CandidateInCertificate(TimeStampedModel):
    score = models.DecimalField(max_digits=5, decimal_places=2)
    certificate = models.ForeignKey(ElegibilityCertificate, related_name='candidates')
    candidate = models.ForeignKey(Candidate, related_name='certificates')
    certificate_result = models.ForeignKey(CertificateResult, null=True)

    def __str__(self):
        return '%s %s' % (self.candidate, self.certificate)


class ContactInfo(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, related_name='contact_info')
    number = models.CharField(max_length=15,blank=True)
    email = models.EmailField(blank=True)
    instructions = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    valid = models.BooleanField(default=True)

    def get_info(self):
        if self.number:
            return (_('Phone'), self.number)
        elif self.email:
            return (_('Email'), self.email)

    def __str__(self):
        type, contact = self.get_info()
        return '%s %s %s' % (self.candidate, type, contact)


class ContactAttempt(TimeStampedModel):
    contact_method = models.ForeignKey(ContactInfo)
    succesful_contact = models.BooleanField()
    contact_datetime = models.DateTimeField()
    comments = models.TextField()
    contacted_by = models.ForeignKey(Employee)

