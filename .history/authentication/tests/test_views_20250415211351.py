import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import Application
from django.core.files.uploadedfile import SimpleUploadedFile

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
    application = Application.objects.get(user=user)

    # Mock data that you're expecting in the PersonalInfoForm
    form_data = {
        'first_name': 'Tim',  # Replace these with actual field names from PersonalInfoForm
        'last_name': 'Guinevere',
        'date_of_birth': '2001-12-20',
        'gender': 'male' ,
        'national_id': '50-2012907C50',
        'title': 'mr',
        'marital_status':'single',
        'place_of_birth':'Mutare',
        'citizenship': 'Zimbabwean',
        'country': 'Zimbabwe',
        'disability': 'None',
        'disability_details':'None',
        
       
    }

    # Submit step 2 with form data
    response = logged_in_client.post(reverse('application_view') + '?step=2', data=form_data)

    assert response.status_code == 302  # Check for redirect after form submission
    assert response.url == reverse('application_view') + '?step=3'
    assert Application.objects.filter(user=user).exists()
    
    # You also might want to check if specific fields in application were updated
    application.refresh_from_db()
    assert application.first_name == form_data['first_name']  # Check if the first_name updated correctly
    assert application.last_name == form_data['last_name']  # Check if the last_name updated correctly
    
    
    ##Testing document upload.
@pytest.mark.django_db
def test_application_view_step_three_post(logged_in_client, user):
    # Step 1: Create an application and populate user info
    logged_in_client.post(reverse('application_view') + '?step=1', data={'application_type': 'masters'})

    # Prepare the document files as SimpleUploadedFile
    id_document = SimpleUploadedFile(
        name='id_document.pdf',
        content=b'This is a test file for the ID document',  # This is where you would include the file's binary content
        content_type='application/pdf'  # Ensure you set the correct content type
    )
    birth_certificate = SimpleUploadedFile(
        name='birth_certificate.pdf',
        content=b'This is a test file for the birth certificate',
        content_type='application/pdf'
    )
    
    # Step 3: Use the prepared files to submit the document upload
    form_data = {
        'id_document': id_document,  
        'birth_certificate': birth_certificate,
    }
    
    response = logged_in_client.post(reverse('application_view') + '?step=3', data=form_data, follow=True)
    assert response.status_code == 200  # Expecting a 200 OK response
    assert response.url == reverse('application_view') + '?step=4'

