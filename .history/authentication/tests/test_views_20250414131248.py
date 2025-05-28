import pytest
from django.urls import reverse
from django.contrib.auth.models import User
#from authentication.models import Application, Documents, Contact, Other, EducationalBackgroundMasters, EducationalBackgroundCertificate, WorkExperience
#from authentication.forms import ProgramTypeForm, PersonalInfoForm, DocumentUploadForm, ContactAndAddressForm

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')
  
@pytest.fixture
def logged_in_client(client, user):
    client.login(username='testuser', password='testpassword')
    return client 
  
@pytest.mark.django_db #using django database for this test
def test_application_view_step_one(logged_in_client):
  response = logged_in_client.get(reverse('authentication:application_view' + ':step_1'))
  assert response.status_code == 200
  assert 'program_selection.html' in str(response.content)
  
