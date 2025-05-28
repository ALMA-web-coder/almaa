from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Application, Contact, MastersEducational, WorkExperience, Other, Status, Documents
from .forms import (
    PersonalInfoForm,
    DocumentUploadForm,
    ContactAndAddressForm,
    EducationalBackgroundMastersForm,
    MastersEducationalDocumentForm,
    WorkExperienceForm,
    OtherInfoForm,
)
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

class MastersApplicationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('masters_application')

    def test_get_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/masters_application.html')
        self.assertIsInstance(response.context['personal_info_form'], PersonalInfoForm)
        self.assertIsInstance(response.context['documents_upload_form'], DocumentUploadForm)
        self.assertIsInstance(response.context['contact_and_address_form'], ContactAndAddressForm)
        self.assertIsInstance(response.context['educational_form'], EducationalBackgroundMastersForm)
        self.assertIsInstance(response.context['document_upload_form'], MastersEducationalDocumentForm)
        self.assertIsInstance(response.context['work_experience_form'], WorkExperienceForm)
        self.assertIsInstance(response.context['other_info_form'], OtherInfoForm)

@pytest.mark.django_db
def test_post_request_with_invalid_data(client):
    # Create a test user
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    # Create test files with valid content
    test_file = SimpleUploadedFile(
        name="test.pdf",
        content=b"This is a dummy PDF file content.",
        content_type="application/pdf"
    )
    
    form_data = {
        # PersonalInfoForm fields
        'first_name': '',  # Empty required field
        'last_name': '',   # Empty required field
        'date_of_birth': '1990-01-01',
        'gender': 'male',
        'national_id': '1234567890',
        'title': 'mr',
        'marital_status': 'single',
        'place_of_birth': '',  # Empty required field
        'citizenship': '',     # Empty required field
        'country': 'USA',
        'disability': '',
        'disability_details': '',
        
        # ContactAndAddressForm fields
        'phone_number': '1234567890',
        'email': 'john.doe@example.com',
        'permanent_address_no_street': '123 Main St',
        'permanent_address_apt_unit': 'Apt 4B',
        'permanent_address_state_province': 'NY',
        'home_phone': '0987654321',
        'office_phone': '5555555555',
        
        # EducationalBackgroundMastersForm fields
        'awarding_institution': '',  # Empty required field
        'degree_diploma_level_classification': 'First Class',
        'major_subjects': 'Computer Science',
        'date_awarded': '2015-05-15',
        'programme_applied_for': 'MBA',
        'preferred_learning_format': 'online',
        'prospective_sponsors': 'Self',
        
        # WorkExperienceForm fields
        'employer': 'Tech Corp',
        'work_details': 'Software Engineer',
        'work_experience_from': '2016-01-01',
        'work_experience_to': '2020-12-31',
        'reference_1_name': 'Jane Smith',
        'reference_1_email': 'jane.smith@example.com',
        'reference_1_phone_number': '1111111111',
        'reference_2_name': 'John Smith',
        'reference_2_email': 'john.smith@example.com',
        'reference_2_phone_number': '2222222222',
        
        # OtherInfoForm fields
        'how_did_you_hear_about_ALMA': 'From a friend',
        'additional_remarks': 'Looking forward to joining!'
    }
    
    # Create a dictionary for file uploads
    files = {
        'id_document': test_file,
        'birth_certificate': test_file,
        'transcript': test_file,
        'degree_certificate': test_file,
        'a_level_certificate': test_file,
        'o_level_certificate': test_file,
        'CV': test_file,
    }
    
    url = reverse('masters_application')
    response = client.post(url, data=form_data, files=files, format='multipart')
    
    # Debugging: Print detailed information
    if response.status_code != 200:
        print("\n===== Debugging Information =====")
        print("Response status code:", response.status_code)
        print("Expected status code: 200 (Form re-rendered with errors)")
        print("Form errors:")
        for context in response.context:
            if hasattr(context, 'errors'):
                print(f"Form errors:", context.errors)
        print("Context data:", response.context)
        print("===============================\n")
    
    # Verify the form submission fails
    assert response.status_code == 200, "Expected a 200 but got status code 302. Check the debugging output above for details."
    
    # Verify no application is created
    application = Application.objects.first()
    assert application is None, "Application should not be created with invalid data."
    
    # Verify related models are not created
    assert Contact.objects.count() == 0
    assert MastersEducational.objects.count() == 0
    assert WorkExperience.objects.count() == 0
    assert Other.objects.count() == 0
    assert Status.objects.count() == 0
    assert Documents.objects.count() == 0
