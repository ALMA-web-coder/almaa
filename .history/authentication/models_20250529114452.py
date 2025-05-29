from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from authentication.signals import update_status
import datetime




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
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    # date_of_birth remains required with a default date
    date_of_birth = models.DateField(default=datetime.date(2001, 12, 12), blank=False, null=False )
    gender = models.CharField(max_length=10, blank=False, null=False)
    national_id = models.CharField(max_length=25, blank=False, null=False)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=False, null=False)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=False, null=False)
    citizenship = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    disability = models.BooleanField(default=False)
    disability_details = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.application_type}"

class Contact(models.Model):
    application = models.ForeignKey(Application, related_name='contacts', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    permanent_address_no_street = models.CharField(max_length=255, blank=False, null=False)
    permanent_address_apt_unit = models.CharField(max_length=255, blank=False, null=False)
    permanent_address_state_province = models.CharField(max_length=100, blank=False, null=False)
    home_phone = models.CharField(max_length=15, blank=False, null=False)
    office_phone = models.CharField(max_length=15, blank=False, null=False)

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
    period_of_study = models.CharField(max_length=100, blank=False, null=False)
    awarding_institution = models.CharField(max_length=100, blank=False, null=False)
    degree_diploma_level_classification = models.CharField(max_length=100, blank=False, null=False)
    major_subjects = models.CharField(max_length=255, blank=False, null=False)
    # date_awarded remains required with a default date
    date_awarded = models.DateField(default=datetime.date(2001, 12, 12), blank=False, null=False )
    preferred_learning_format = models.CharField(max_length=10, choices=LEARNING_FORMAT_CHOICES, blank=False, null=False)
    programme_applied_for = models.CharField(max_length=100, choices=PROGRAMME_CHOICES, blank=False, null=False)
    prospective_sponsors = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.degree_diploma_level_classification} from {self.awarding_institution} for {self.application.first_name} {self.application.last_name}"


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
    period_of_study = models.CharField(max_length=100, blank=False, null=False)
    institution_attended = models.CharField(max_length=110, blank=False, null=False)
    level_of_study = models.CharField(max_length=100, blank=False, null=False)
    major_subjects = models.CharField(max_length=100, blank=False, null=False)
    # date_awarded remains required with a default date
    date_awarded = models.DateField(default=datetime.date(2001, 12, 12), blank=False, null=False)
    programme_applied_for = models.CharField(max_length=100, choices=PROGRAMME_CHOICES, blank=False, null=False)
    preferred_learning_format = models.CharField(max_length=10, choices=LEARNING_FORMAT_CHOICES, blank=False, null=False)
    prospective_sponsors = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.get_programme_applied_for_display()} from {self.institution_attended} for {self.application.first_name} {self.application.last_name}"

class Other(models.Model):
    application = models.ForeignKey(Application, related_name='other', on_delete=models.CASCADE)
    how_did_you_hear_about_ALMA = models.CharField(max_length=255, blank=False, null=False)
    additional_remarks = models.TextField(blank=True, null=True)

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
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to now when saved

    @property
    def last_update(self):
        return self.updated_at

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the signal is only connected once
        if not hasattr(self.__class__, '_post_save_connected'):
            post_save.connect(update_status, sender=self.__class__)
            self.__class__._post_save_connected = True


    def __str__(self):
        return f"{self.application}: {self.status}"

class WorkExperience(models.Model):
    application = models.ForeignKey(Application, related_name='work_experiences', on_delete=models.CASCADE)
    employer = models.CharField(max_length=100, blank=False, null=False)
    work_details = models.TextField(blank=False, null=False)
    # work_experience_from remains required with a default date
    work_experience_from = models.DateField(default=datetime.date(2000, 12, 12), blank=False, null=False)
    # work_experience_to remains required with a default date
    work_experience_to = models.DateField(default=datetime.date(2001, 12, 12), blank=False, null=False )
    reference_1_name = models.CharField(max_length=100, blank=False, null=False)
    reference_1_email = models.EmailField(max_length=50, blank=False, null=False)
    reference_1_phone_number = models.CharField(max_length=15, blank=False, null=False)
    reference_2_name = models.CharField(max_length=100, blank=False, null=False)
    reference_2_email = models.EmailField(max_length=50, blank=False, null=False)
    reference_2_phone_number = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self):
        return f"Work Experience at {self.employer} for {self.application.first_name} {self.application.last_name}"


class Documents(models.Model):
    application = models.ForeignKey(Application, related_name='documents', on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to='documents/birth_certificates/', blank=False, null=False)
    id_document = models.FileField(upload_to='documents/id_documents/', blank=False, null=False)

    def __str__(self):
        return f"Documents for {self.application.first_name} {self.application.last_name}"

class MastersDocuments(models.Model):
    application = models.ForeignKey(Application, related_name='masters', on_delete=models.CASCADE)
    transcript = models.FileField(upload_to='documents/transcript',blank=False)
    degree_certificate = models.FileField (upload_to='documents/degree_certificate',blank=False)
    a_level_certificate = models.FileField (upload_to='documents/a_level_certificate',blank=False)
    o_level_certificate = models.FileField(upload_to='documents/o_level_certificate',blank=False)
    CV = models.FileField(upload_to='documents/CV' ,blank=False)

    def __str__(self):
        return f"MastersDocuments for {self.application.first_name} {self.application.last_name}"

class CertificateDocuments(models.Model):
    application = models.ForeignKey(Application, related_name='certificate', on_delete=models.CASCADE)
    a_level_certificate = models.FileField (upload_to='documents/a_level_certificate',blank=False)
    o_level_certificate = models.FileField(upload_to='documents/o_level_certificate',blank=False)
    CV = models.FileField(upload_to='documents/CV' ,blank=False)

    def __str__(self):
        return f"CertificateDocuments for {self.application.first_name} {self.application.last_name}"



class Download(models.Model):
    download = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Download {self.id}"


class ApplicationPayments(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('application_fee', 'APPLICATION FEE PAYMENT'),

    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    paynow_reference = models.CharField(max_length=100, blank=False, null=False)
    redirect_url = models.URLField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, blank=False, null=False)
    customer_email = models.EmailField(blank=False, null=False)
    customer_name = models.CharField(max_length=100, blank=False, null=False)
    customer_phone = models.CharField(max_length=20, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    reference = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paynow_reference} - {self.status}"

class GeneralPayments(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('fees', 'FEES PAYMENT'),
        ('tuition', 'TUITION PAYMENT'),
        ('donation', 'DONATIONS'),
        ('other', 'OTHER'),
    ]

    paynow_reference = models.CharField(max_length=100, blank=False, null=False)
    redirect_url = models.URLField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, blank=False, null=False)
    status = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='pending') # Corrected status choices here
    customer_email = models.EmailField(blank=False, null=False)
    customer_name = models.CharField(max_length=100, blank=False, null=False)
    customer_phone = models.CharField(max_length=20, blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    reference = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paynow_reference} - {self.status}"