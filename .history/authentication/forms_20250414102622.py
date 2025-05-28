from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Application, CertificateDocuments, CertificateEducational, Contact, MastersDocuments, MastersEducational, Other, Status, WorkExperience, Documents
import datetime




class ProgramTypeForm(forms.Form):
    CHOICES = [
        ('masters', 'Masters'),
        ('certificate', 'Certificate')
    ]
    application_type = forms.ChoiceField(choices=CHOICES, label="Choose Program Type")


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'national_id', 'title', 'marital_status',
            'place_of_birth', 'citizenship', 'country',
            'disability', 'disability_details'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'gender':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID'}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place of Birth'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizenship'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'disability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disability_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Details about disability'}),
        }
        
    def clean_date_of_birth(self):
        date_of_birth =  self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > datetime.date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth
        
        
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['id_document', 'birth_certificate']
        widgets = {
            'id_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'birth_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_id_document(self):
        id_document = self.cleaned_data.get('id_document')
        if id_document:
            if not id_document.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return id_document
    def clean_birth_certificate(self):
        birth_certificate = self.cleaned_data.get('birth_certificate')
        if birth_certificate:
            if not birth_certificate.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return birth_certificate

class ContactAndAddressForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'phone_number', 'email', 
            'permanent_address_no_street', 
            'permanent_address_apt_unit', 
            'permanent_address_state_province', 
            'home_phone', 'office_phone'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'permanent_address_no_street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Number and Name'}),
            'permanent_address_apt_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apt/Unit'}),
            'permanent_address_state_province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'home_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Home Phone'}),
            'office_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office Phone'}),
        }
        
class EducationalBackgroundMastersForm(forms.ModelForm):
    class Meta:
        model = MastersEducational
        fields = [
            'awarding_institution', 
            'degree_diploma_level_classification', 
            'major_subjects', 
            'date_awarded',
            'programme_applied_for',  
            'preferred_learning_format', 
            'prospective_sponsors'
        ]
        widgets = {
            'awarding_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Awarding Institution'}),
            'degree_diploma_level_classification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Upper Second Class'}),
            'major_subjects': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major Subjects'}),
            'date_awarded': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'programme_applied_for': forms.Select(attrs={'class': 'form-select'}),
            'preferred_learning_format': forms.Select(attrs={'class': 'form-select'}),
            'prospective_sponsors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. self'}),
        }
        
class MastersEducationalDocumentForm(forms.ModelForm):
    class Meta:
        model = MastersDocuments
        fields = [
            'transcript', 
            'degree_certificate', 
            'CV', 
            'a_level_certificate', 
            'o_level_certificate'
        ]
        widgets = {
            'transcript': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'degree_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'CV': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'a_level_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'o_level_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class EducationalBackgroundCertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateEducational
        fields = [
            'period_of_study',
            'institution_attended',
            'level_of_study',
            'major_subjects',
            'date_awarded',
            'programme_applied_for', 
            'preferred_learning_format', 
            'prospective_sponsors'
        ]
        widgets = {
            'period_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Period of Study'}),
            'institution_attended': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution Attended'}),
            'level_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Level of Study'}),
            'major_subjects': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major Subjects'}),
            'date_awarded': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'programme_applied_for': forms.Select(attrs={'class': 'form-select'}),
            'preferred_learning_format': forms.Select(attrs={'class': 'form-select'}),
            'prospective_sponsors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. self'}),
        }

class CertificateEducationalDocumentForm(forms.ModelForm):
    class Meta:
        model = CertificateDocuments
        fields = ['a_level_certificate', 'o_level_certificate', 'CV']
        widgets = {
            'a_level_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'o_level_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'CV': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = [
            'employer',
            'work_details',
            'work_experience_from',
            'work_experience_to',
            'reference_1_name',
            'reference_1_email',
            'reference_1_phone_number',
            'reference_2_name',
            'reference_2_email',
            'reference_2_phone_number'
        ]

    def __init__(self, *args, **kwargs):
        super(WorkExperienceForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        work_experience_from = cleaned_data.get('work_experience_from')
        work_experience_to = cleaned_data.get('work_experience_to')

        if work_experience_from and work_experience_to:
            if work_experience_from > work_experience_to:
                raise forms.ValidationError("The start date cannot be after the end date.")

        return cleaned_data

class OtherInfoForm(forms.ModelForm):
    class Meta:
        model = Other
        fields = ['how_did_you_hear_about_ALMA', 'additional_remarks']
        widgets = {
            'how_did_you_hear_about_ALMA': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
            'additional_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'True'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True'
        })



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': True
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': True
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': True
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': True
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype Password',
            'required': True
        })

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Initialize an error message list
        errors = []

        # Check password length
        if password1 and len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            errors.append('The two password fields didn’t match.')

        # Add all errors to the appropriate fields
        for error in errors:
            self.add_error('password1', error)

        return cleaned_data


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True'
        })


class ResetPasswordConfirmForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password',
            'required': 'True'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype New Password',
            'required': 'True'
        })
