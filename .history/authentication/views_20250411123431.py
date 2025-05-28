# import this to require login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# import this for sending email to user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime
from paynow import Paynow  # Import the Paynow class

from authentication.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import Group
from .models import Application, Contact, Documents, WorkExperience, Other
from django.shortcuts import render, get_object_or_404
from django import forms
from django.urls import reverse
from django.conf import settings
from .forms import (
    CertificateEducationalDocumentForm,
    DocumentUploadForm,
    EducationalBackgroundCertificateForm,
    EducationalBackgroundMastersForm,
    MastersEducationalDocumentForm,
    ProgramTypeForm,
    StatusForm,
    UserLoginForm,
    UserRegistrationForm,
    PersonalInfoForm,
    ContactAndAddressForm,
    WorkExperienceForm,
    OtherInfoForm,
    
)


# Create your views here.

def application_list(request):
    applications = Application.objects.all()  # Fetch all applications
    return render(request, 'application/application_list.html', {'applications': applications})



def application_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    return render(request, 'application/application_detail.html', {'application': application})



@login_required(login_url='login')
def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Assign user to the "Student" group
            try:
                student_group = Group.objects.get(name='Students')
                student_group.user_set.add(user)  # Add the user to the group
            except Group.DoesNotExist:
                # Handle the case if the group does not exist
                messages.error(request, 'User group not found. Please contact support.')

            # email user with activation link
            current_site = get_current_site(request)
            mail_subject = "Activate your account."

            # the message will render what is written in authentication/email_activation/activate_email_message.html
            message = render_to_string('authentication/email_activation/activate_email_message.html', {
                'user': form.cleaned_data['username'],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Account created successfully. Please check your email to activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Account creation failed. Please try again! Password should be at least 8 characters long and include a mix of letters, numbers, and special characters.')

    return render(request, 'authentication/register.html', {
        'form': form
    })
# to activate user from email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/email_activation/activation_successful.html')
    else:
        return render(request, 'authentication/email_activation/activation_unsuccessful.html')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Successful login
                login(request, user)  # Log the user in

                # Check user group and redirect accordingly
                if user.groups.filter(name='Registrar').exists():
                    return redirect('application_list')  # Redirect for Registrars
                elif user.groups.filter(name='Students').exists():
                    return redirect('homepage')  # Redirect for Students
                else:
                    # Redirect or message for users not in the specified groups
                    messages.warning(request, 'You do not have permission to access this application.')
                    return redirect('login')  # Redirect back to login or another page
            else:
                messages.error(request, 'Invalid username or password.')  # Invalid credentials
        else:
            # Handle form errors by sending feedback to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    else:
        form = UserLoginForm()  # Initialize empty form for GET requests

    # Render the login template with the form
    return render(request, 'authentication/login.html', {'form': form})



@login_required
def application_view(request):
    user = request.user
    step = request.GET.get('step', '1')
    
    # Handle the first step of the process: selecting application type
    if step == '1':
        return step_one_handler(request, user)

    # Retrieve the user's most recent application only for the next steps
    application = Application.objects.filter(user=user).last()

    # Ensure an application exists for further steps
    if application is None:
        return redirect(reverse('authentication:application_view') + '?step=1')

    # Map steps to their corresponding handlers
    step_handlers = {
        '2': step_two_handler,
        '3': step_three_handler,
        '4': step_four_handler,
        '5': step_five_handler,
        '6': step_six_handler,
        '7': step_seven_handler,
        '8': step_eight_handler,
        '9': payment_handler,
        '10': step_nine_handler,
    }

    # Call the appropriate handler based on the current step
    if step in step_handlers:
        return step_handlers[step](request, application)
    else:
        return redirect(reverse('application_view') + '?step=1')


def step_one_handler(request, user):
    form = ProgramTypeForm(request.POST or None)  # Use POST data if available
    if request.method == 'POST':
        if form.is_valid():
            application = Application(user=user)
            application.application_type = form.cleaned_data['application_type']
            application.save()
            return redirect(reverse('application_view') + '?step=2')
    return render(request, 'application/program_selection.html', {'form': form})

def step_two_handler(request, application):
    form = PersonalInfoForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('application_view') + '?step=3')
    return render(request, 'application/personal.html', {'form': form})

def step_three_handler(request, application):
    documents, _ = Documents.objects.get_or_create(application=application)

    form = DocumentUploadForm(request.POST or None, request.FILES or None, instance=documents)
    if request.method == 'POST' and form.is_valid():
        documents = form.save()
        return redirect(reverse('application_view') + '?step=4')

    return render(request, 'application/personal_document.html', {'form': form})

def step_four_handler(request, application):
    contact, _ = Contact.objects.get_or_create(application=application)

    form = ContactAndAddressForm(request.POST or None, instance=contact)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('application_view') + '?step=5')

    return render(request, 'application/contact_and_address.html', {'form': form})

def step_five_handler(request, application):
    form_class = EducationalBackgroundMastersForm if application.application_type == 'masters' else EducationalBackgroundCertificateForm
    
    # existing_instance = application.educational.first() if application.educational.exists() else None
    
    template_name = 'application/masters_educational_background.html' if application.application_type == 'masters' else 'application/certificate_educational_background.html'
    existing_instance = application.educational.first() if application.educational.exists() else None
        
    form = form_class(request.POST or None, instance=existing_instance)
    if request.method == 'POST' and form.is_valid():
        educational = form.save(commit=False)
        educational.application = application
        educational.save()
        return redirect(reverse('application_view') + '?step=6')

    print(form.errors)
    return render(request, template_name, {'form': form})

def step_six_handler(request, application):
    if application.application_type == 'masters':
        form_class = MastersEducationalDocumentForm 
        template_name = 'application/mastersdoc.html'
        existing_instance = application.masters.first() if application.masters.exists() else None
    else:  # Certificates
        form_class = CertificateEducationalDocumentForm  
        template_name = 'application/certificatedoc.html'
        existing_instance = application.certificate.first() if application.certificate.exists() else None

    form = form_class(request.POST or None, request.FILES or None, instance=existing_instance)
    if request.method == 'POST' and form.is_valid():
        educational = form.save(commit=False)
        educational.application = application
        educational.save()
        return redirect(reverse('application_view') + '?step=7')

    return render(request, template_name, {'form': form})

def step_seven_handler(request, application):
    WorkExperienceFormSet = forms.inlineformset_factory(Application, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=False)
    formset = WorkExperienceFormSet(request.POST or None, queryset=application.work_experiences.all())
    if request.method == 'POST' and formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            instance.application = application
            instance.save()
        return redirect(reverse('application_view') + '?step=8')

    return render(request, 'application/work_experience.html', {'formset': formset})

def step_eight_handler(request, application):
    other, _ = Other.objects.get_or_create(application=application)

    form = OtherInfoForm(request.POST or None, instance=other)
    if request.method == 'POST':
        if form.is_valid():
            other_info = form.save()  # No need to commit=False then save again.  form.save() handles everything

            return redirect(reverse('application_view') + '?step=9')
        else:
            print(form.errors)  # Print form errors to the console for debugging

    return render(request, 'application/other.html', {'form': form})

# Payment handling code here remains unchanged
def check_payment_status(paynow, response, application):
    """Check the payment status using the poll URL."""
    status = paynow.check_transaction_status(response.poll_url)
    if status.paid:
        application.is_paid = True
        application.save()
        return True
    return False


def payment_handler(request, application):
    paynow = Paynow(
        settings.PAYNOW['INTEGRATION_ID'],
        settings.PAYNOW['INTEGRATION_KEY'],
        settings.PAYNOW['RESULT_URL'],
        settings.PAYNOW['RETURN_URL']
    )
    context = {  # Define context here
        'application': application  # Optionally pass the application object to the template
    }
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        payment = paynow.create_payment('Application Fee', 'moses.chundu@cccsea.org')
        payment.add('Application Fee Payment', 20)

        if payment_method == 'mobile':
            response = paynow.send_mobile(payment, '0771111111', 'ecocash')
            print(f"Mobile Payment Response: {response.__dict__}")

            if response.success:
                payment_successful = check_payment_status(paynow, response, application) # Call method to change application.is_paid

                if payment_successful:
                    messages.success(request, 'Payment successful.')
                    return redirect('application_success')
            else:
                messages.error(request, 'Mobile payment failed. Please try again.')

        elif payment_method == 'card':
            response = paynow.send(payment)
            print(f"Card Payment Response: {response.__dict__}")

            if response.success:
                if response.has_redirect:
                    messages.info(request, 'Payment is still pending. Please complete the payment.')
                    return redirect(response.redirect_url)
                else:
                    messages.error(request, 'Card payment didn\'t redirect. Please contact support.')
            else:
                messages.error(request, 'Card payment failed. Please try again.')

    return render(request, 'application/payment.html', context)

def step_nine_handler(request, application):
    return render(request, 'application/success.html', {
        'current_year': datetime.now().year,
        'email': request.user.email,
    })
    
    
def track_application(request):
    application = None
    latest_status = None
    error_message = None
    
    if request.method == 'POST':
        national_id = request.POST.get('national_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        try:
            
            application = Application.objects.get(
                national_id=national_id,
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
            
            latest_status = application.statuses.order_by('-id').first()  
        except Application.DoesNotExist:
            error_message = "No application found with the provided details."

    
    return render(request, 'application/track_application.html', {
        'application': application,
        'latest_status': latest_status,
        'error_message': error_message
    })
    
    
@login_required 
def update_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    
    status, created = Status.objects.get_or_create(application=application)
    
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()  
            return redirect('application_detail', application_id=application.id) 
    else:
        form = StatusForm(instance=status)

    return render(request, 'application/update_status.html', {'form': form, 'application': application})
    