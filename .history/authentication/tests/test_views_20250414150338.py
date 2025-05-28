import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import Application
# Documents, Contact, Other, EducationalBackgroundMasters, EducationalBackgroundCertificate, WorkExperience
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

@pytest.mark.django_db
def test_application_view_step_two(logged_in_client)
##creating an application in step 1

logged_in_client.post(reverse('application_view') + '?step=1', data={'application_type': 'masters'})

application = Application.objecta.get(user=logged_in_client.request.user)
response = logged_in_client.post(reverse('application_view') + '?step=2')

assert response.status_code == 200
assert 'application/personal.html' in str(response.content)  

   # Test form submission
response = logged_in_client.post(reverse('authentication:application_view') + '?step=2', {
        'field1': 'value1',  # Replace with actual form fields
        'field2': 'value2',
    })
    
assert response.status_code == 302  # Check for redirect after form submission
assert Application.objects.filter(user=logged_in_client.request.user).exists() 