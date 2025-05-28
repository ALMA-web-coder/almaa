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
def test_application_view_step_two(logged_in_client, user):
    # Step 1: Create an application
    logged_in_client.post(reverse('application_view') + '?step=1', data={'application_type': 'masters'})

    # Fetch the created application instance
    application = Application.objects.get(user=logged_in_client.request.user)

    # Mock data that you're expecting in the PersonalInfoForm
    form_data = {
        'first_name': 'Tim',  # Replace these with actual field names from PersonalInfoForm
        'last_name': 'Panashe',
        'email': 'guine@example.com',
        # include any other fields required by the form...
    }

    # Submit step 2 with form data
    response = logged_in_client.post(reverse('application_view') + '?step=2', data=form_data)

    assert response.status_code == 302  # Check for redirect after form submission
    assert response.url == reverse('application_view') + '?step=3'
    assert Application.objects.filter(user=logged_in_client.request.user).exists()
    
    # You also might want to check if specific fields in application were updated
    application.refresh_from_db()
    assert application.first_name == form_data['first_name']  # Check if the first_name updated correctly
    assert application.last_name == form_data['last_name']  # Check if the last_name updated correctly