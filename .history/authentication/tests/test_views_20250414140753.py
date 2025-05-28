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
  
@pytest.mark.django_db
def test_application_view_step_one_post(logged_in_client):
    response = logged_in_client.post(reverse('application_view') + '?step=1', data={'application_type': 'masters'})
    assert response.status_code == 302  
    assert response.url == reverse('application_view') + '?step=2'
