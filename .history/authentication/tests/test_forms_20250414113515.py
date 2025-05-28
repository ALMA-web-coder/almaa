import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.forms import (
    ProgramTypeForm,
    PersonalInfoForm,
    DocumentUploadForm,
    ContactAndAddressForm,
    EducationalBackgroundMastersForm,
    EducationalBackgroundCertificateForm,
    WorkExperienceForm,
    OtherInfoForm,
    UserLoginForm
)

from authentication.models import (
  Application, Documents, Contact, Other
)


@pytest.mark.django_db
def test_personal_info_form():
  user = User.objects.create_user(
    username='testuser', password='testpassword'
  )
  
  application = Application.objects.create(user=user)
  
  form_data = {
    'first_name': 'Guinevere',
    'last_name': 'Tim',
    'date_of_birth': '2024-01-01',
    'gender': 'Female',
    'national_id' : '50-2012907C50',
    'title': 'ms',
    'marital_status': 'single',
    'place_of_birth': 'Harare',
    'citizenship': 'Zimbabwean',
    'country': 'Zimbabwe',
    'disability': 'None',
    'disability_description': 'None',
  }
  
  form = PersonalInfoForm(data=form_data, instance=application)
  assert form.is_valid(), form.errors
  
  form_data_invalid ={**form_data, 'date_of_birth': '2027-01-01'} #Using a future date
  form_invalid = PersonalInfoForm(data=form_data_invalid, instance=application)
  assert not form_invalid.is_valid()
  assert 'Date of birth cannot be in the future.' in form_invalid.errors['date_of_birth']
  