from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Application, CertificateDocuments, CertificateEducational, Contact, MastersDocuments, MastersEducational, Other, Status, WorkExperience, Documents
import datetime
import re
from django.core.exceptions import ValidationError




class ProgramTypeForm(forms.Form):
    application_type = forms.ChoiceField(choices=[('masters', 'Masters'), ('certificate', 'Certificate')])


class PersonalInfoForm(forms.ModelForm):
    TITLE_CHOICES = [
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
    ('ms', 'Ms.'),
    ('dr', 'Dr.'),
]
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
            'disability': forms.CheckboxInput(attrs={'class': 'form-check-input', 'column':2,}),
            'disability_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Details about disability'}),
           
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
            'id_document': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
            'birth_certificate': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            })
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
            'phone_number', 
            'email', 
            'permanent_address_no_street', 
            'permanent_address_apt_unit', 
            'permanent_address_state_province', 
            'home_phone', 
            'office_phone'
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
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if not phone_number.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(phone_number) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone_number
    def clean_home_phone(self):
        home_phone = self.cleaned_data.get('home_phone')
        if home_phone:
            if not home_phone.isdigit():
                raise forms.ValidationError("Home phone number must contain only digits.")
            if len(home_phone) < 10:
                raise forms.ValidationError("Home phone number must be at least 10 digits long.")
        return home_phone
    def clean_office_phone(self):
        office_phone = self.cleaned_data.get('office_phone')
        if office_phone:
            if not office_phone.isdigit():
                raise forms.ValidationError("Office phone number must contain only digits.")
            if len(office_phone) < 10:
                raise forms.ValidationError("Office phone number must be at least 10 digits long.")
        return office_phone
        
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
            'period_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Period of Study'}),
            'awarding_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Awarding Institution'}),
            'degree_diploma_level_classification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Upper Second Class'}),
            'major_subjects': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major Subjects'}),
            'date_awarded': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'programme_applied_for': forms.Select(attrs={'class': 'form-select'}),
            'preferred_learning_format': forms.Select(attrs={'class': 'form-select'}),
            'prospective_sponsors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. self'}),
        }
        
    def clean_date_awarded(self):
        date_awarded = self.cleaned_data.get('date_awarded')
        if date_awarded and date_awarded > datetime.date.today():
            raise forms.ValidationError("Date awarded cannot be in the future.")
        return date_awarded
        
class MastersEducationalDocumentForm(forms.ModelForm):
    class Meta:
        model = MastersDocuments
        fields = ['transcript', 'degree_certificate', 'CV', 'a_level_certificate', 'o_level_certificate']
        widgets = {
            'transcript': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
            'degree_certificate': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
            'CV': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
            'a_level_certificate': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
            'o_level_certificate': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.png',
                'class': 'form-control',
                'style': 'cursor: pointer;'
            }),
        }

    def clean_transcript(self):
        transcript = self.cleaned_data.get('transcript')
        if transcript:
            if not transcript.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return transcript

    def clean_degree_certificate(self):
        degree_certificate = self.cleaned_data.get('degree_certificate')
        if degree_certificate:
            if not degree_certificate.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return degree_certificate

    def clean_CV(self):
        CV = self.cleaned_data.get('CV')
        if CV:
            if not CV.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return CV

    def clean_a_level_certificate(self):
        a_level_certificate = self.cleaned_data.get('a_level_certificate')
        if a_level_certificate:
            if not a_level_certificate.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return a_level_certificate

    def clean_o_level_certificate(self):
        o_level_certificate = self.cleaned_data.get('o_level_certificate')
        if o_level_certificate:
            if not o_level_certificate.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, and PNG files are allowed.")
        return o_level_certificate

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
        
    def clean_date_awarded(self):
        date_awarded = self.cleaned_data.get('date_awarded')
        if date_awarded and date_awarded > datetime.date.today():
            raise forms.ValidationError("Date awarded cannot be in the future.")
        return date_awarded

        
class CertificateEducationalDocumentForm(forms.ModelForm):
    class Meta:
        model= CertificateDocuments
        fields = ['a_level_certificate', 'o_level_certificate', 'CV']

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
        widgets = {
            'work_experience_from': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'work_experience_to': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'employer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employer'}),
            'work_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Work Details'}),
            'reference_1_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Name'}),
            'reference_1_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Email'}),
            'reference_1_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 1 Phone Number'}),
            'reference_2_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Name'}),
            'reference_2_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Email'}),
            'reference_2_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference 2 Phone Number'}),
            
        }
        
    def reference_1_phone_number(self):
        reference_1_phone_number = self.cleaned_data.get('reference_1_phone_number')
        if reference_1_phone_number:
            if not reference_1_phone_number.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(reference_1_phone_number) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return reference_1_phone_number
    def reference_2_phone_number(self):
        reference_2_phone_number = self.cleaned_data.get('reference_2_phone_number')
        if reference_2_phone_number:
            if not reference_2_phone_number.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            if len(reference_2_phone_number) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return reference_2_phone_number

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

        # Check password complexity
        if password1 and not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password1):
            errors.append('Password should include a mix of letters, numbers, and special characters.')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            errors.append("The two password fields didn't match.")

        # Add all errors to the appropriate fields
        for error in errors:
            self.add_error('password1', error)

        # Raise a validation error if there are any errors
        if errors:
            raise ValidationError("Account creation failed. Please try again!")

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

class PaynowPaymentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    reference = forms.CharField(label='Reference', max_length=100, required=True)
    application_type = forms.ChoiceField(
        label='Application Type',
        choices=[('masters', 'Masters'), ('certificate', 'Certificate')],
        required=True
    )
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Phone Number', max_length=20, required=True)
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=[('mobile', 'Mobile Payment (Ecocash)'), ('card', 'Card Payment')],
        required=True
    )
