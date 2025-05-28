from django.db import models
from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone
from django.db.models.signals import post_save
from authentication.signals import update_status
def user_documents_upload_to(instance, filename):
    # Getting the current date in a desired format, e.g., "YYYY-MM-DD"
    current_date = timezone.now().strftime("%Y-%m-%d")
    # Getting the user's full name (first name and last name)
    user_name = f"{instance.application.first_name}_{instance.application.last_name}"
    # Getting the document type to create a specific folder for each type
    document_type = instance.document_type if hasattr(instance, 'document_type') else 'documents'
    # Returning the path where the file will be stored
    return f'{current_date}/{user_name}/{document_type}/{filename}'



class Application(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('masters', 'Masters'),
        ('certificate', 'Certificate')
    ]
    
    TITLE_CHOICES = [
        ('mr', 'Mr.'), 
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
        ('dr', 'Dr.'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    is_paid = models.BooleanField(default=False)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES, default='masters')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    national_id = models.CharField(max_length=25)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    place_of_birth = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    disability = models.BooleanField(default=False)
    disability_details = models.TextField(blank=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.application_type}"

class Contact(models.Model):
    application = models.ForeignKey(Application, related_name='contacts', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.EmailField(blank=False)
    permanent_address_no_street = models.CharField(max_length=255, blank=False)
    permanent_address_apt_unit = models.CharField(max_length=255, blank=False)
    permanent_address_state_province = models.CharField(max_length=100, blank=False)
    home_phone = models.CharField(max_length=15, blank=True)
    office_phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Contact for {self.application.first_name} {self.application.last_name}"

class MastersEducational(models.Model):
    PROGRAMME_CHOICES = [
        ('MBA', 'MBA (Leadership & Management) (MBALM)'),
        ('MSc', 'MSc. (Governance & Leadership) (MGOVL)'),
    ]

    LEARNING_FORMAT_CHOICES = [
        ('online', 'Online'),
        ('physical', 'Physical'),
    ]

    application = models.ForeignKey(Application, related_name='educational', on_delete=models.CASCADE)
    period_of_study = models.CharField(max_length=100)
    awarding_institution = models.CharField(max_length=100)
    degree_diploma_level_classification = models.CharField(max_length=100)
    major_subjects = models.CharField(max_length=255)
    date_awarded = models.DateField(blank=False)
    preferred_learning_format = models.CharField(max_length=10, choices=LEARNING_FORMAT_CHOICES, blank=True)
    programme_applied_for = models.CharField(max_length=100, choices=PROGRAMME_CHOICES, null=True, blank=True)
    prospective_sponsors = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.degree_diploma_level_classification} from {self.awarding_institution} for {self.application.first_name} {self.application.last_name}"
    
from django.db import models

class CertificateEducational(models.Model):
    PROGRAMME_CHOICES = [
        ('CLM', 'Certificate In Leadership & Management (CLM)'),
        ('CADM', 'Certificate in Agribusiness Development and Management (CADM)'),
    ]

    LEARNING_FORMAT_CHOICES = [
        ('online', 'Online'),
        ('physical', 'Physical'),
    ]

    application = models.ForeignKey(Application, related_name='certificate_edu', on_delete=models.CASCADE)
    period_of_study = models.CharField(max_length=100, null=True, blank=True)
    institution_attended = models.CharField(max_length=110)
    level_of_study = models.CharField(max_length=100, null=True, blank=True)
    major_subjects = models.CharField(max_length=100, null=True, blank=True)
    date_awarded = models.DateField(null=True)
    programme_applied_for = models.CharField(max_length=100, choices=PROGRAMME_CHOICES, null=True, blank=True)
    preferred_learning_format = models.CharField(max_length=10, choices=LEARNING_FORMAT_CHOICES, null=True, blank=True)
    prospective_sponsors = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.get_programme_applied_for_display()} from {self.institution_attended} for {self.application.first_name} {self.application.last_name}"

class Other(models.Model):
    application = models.ForeignKey(Application, related_name='other', on_delete=models.CASCADE)
    how_did_you_hear_about_ALMA = models.CharField(max_length=255, blank=False)
    additional_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Other Information for {self.application.first_name} {self.application.last_name}"


class Status(models.Model):
    application = models.ForeignKey(Application, related_name='statuses', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    comments = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to now when saved

    @property
    def last_update(self):
        return self.updated_at
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        post_save.connect(update_status, sender=self.__class__)

    def __str__(self):
        return f"{self.application}: {self.status}"

class WorkExperience(models.Model):
    application = models.ForeignKey(Application, related_name='work_experiences', on_delete=models.CASCADE)
    employer = models.CharField(max_length=100, blank=False)
    work_details = models.TextField(blank=True)
    work_experience_from = models.DateField(default='2012-01-01', blank=False) 
    work_experience_to = models.DateField(default='2022-12-31', blank=False)   
    reference_1_name = models.CharField(max_length=100, blank=True)
    reference_1_email = models.EmailField(max_length=50, blank=True)
    reference_1_phone_number= models.CharField(max_length=15, blank=True)
    reference_2_name = models.CharField(max_length=100, blank=True)
    reference_2_email = models.EmailField(max_length=50, blank=True)
    reference_2_phone_number= models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Work Experience at {self.employer} for {self.application.first_name} {self.application.last_name}"

class Documents(models.Model):
    application = models.ForeignKey(Application, related_name='documents', on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to=user_documents_upload_to, blank=False)
    id_document = models.FileField(upload_to=user_documents_upload_to, blank=False)

    def __str__(self):
        return f"Documents for {self.application.first_name} {self.application.last_name}"

class MastersDocuments(models.Model):
    application = models.ForeignKey(Application, related_name='masters', on_delete=models.CASCADE)
    transcript = models.FileField(upload_to=user_documents_upload_to, blank=False)
    degree_certificate = models.FileField(upload_to=user_documents_upload_to, blank=False)
    a_level_certificate = models.FileField(upload_to=user_documents_upload_to, blank=False)
    o_level_certificate = models.FileField(upload_to=user_documents_upload_to, blank=False)
    CV = models.FileField(upload_to=user_documents_upload_to, blank=False)

    def __str__(self):
        return f"MastersDocuments for {self.application.first_name} {self.application.last_name}"

class CertificateDocuments(models.Model):
    application = models.ForeignKey(Application, related_name='certificate', on_delete=models.CASCADE)
    degree_certificate = models.FileField(upload_to=user_documents_upload_to, blank=True, null=True)
    a_level_certificate = models.FileField(upload_to=user_documents_upload_to, blank=True, null=True)
    o_level_certificate = models.FileField(upload_to=user_documents_upload_to, blank=True, null=True)
    CV = models.FileField(upload_to=user_documents_upload_to, blank=True, null=True)

    def __str__(self):
        return f"CertificateDocuments for {self.application.first_name} {self.application.last_name}"
  
  


class Download(models.Model):
    download = models.URLField(max_length=255)

    def __str__(self):
        return self.download