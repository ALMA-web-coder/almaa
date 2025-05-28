from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings
import json
logger = logging.getLogger('audit')
from authentication.middleware import get_current_user


@receiver(pre_save, sender='authentication.Status')
def update_status(sender, instance, **kwargs):
    if instance.pk:
        previous = sender.objects.get(pk=instance.pk)
        previous_status = previous.status
    else:
        previous_status = None

    # Only proceed if status has changed
    if previous_status != instance.status:
        # Send email
        subject = 'Status Update Notification'
        message = f'Your status has been updated to: {instance.status}'
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.application.contacts.first().email  # assuming contact exists

        send_mail(subject, message, from_email, [to_email], fail_silently=False)


# Dictionary to temporarily store previous instances
_PREVIOUS_STATE = {}

@receiver(pre_save)
def cache_previous_instance(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Store the old instance state
            _PREVIOUS_STATE[instance.pk] = {
                field.name: getattr(old_instance, field.name)
                for field in sender._meta.fields
            }
        except sender.DoesNotExist:
            pass

@receiver(post_save)
def log_detailed_changes(sender, instance, created, **kwargs):
    user = get_current_user()
    now = timezone.now()

    if created:
        # Log creation
        message = f"{now}: CREATE on {sender.__name__} id={instance.pk} by {user}"
    else:
        # Log update with changed fields
        old_state = _PREVIOUS_STATE.pop(instance.pk, {})
        changed_fields = []

        for field in sender._meta.fields:
            field_name = field.name
            old_value = old_state.get(field_name)
            new_value = getattr(instance, field_name)

            if old_value != new_value:
                changed_fields.append({
                    'field': field_name,
                    'old': old_value,
                    'new': new_value
                })

        if changed_fields:
            # Convert list of changes to JSON string for readability
            changes_json = json.dumps(
    changed_fields,
    default=str  # this converts datetime objects to ISO format strings
)
            message = f"{now}: UPDATE on {sender.__name__} id={instance.pk} by {user}. Changes: {changes_json}"
        else:
            message = f"{now}: UPDATE on {sender.__name__} id={instance.pk} with no changes by {user}"

    # Log the detailed message
    logger = logging.getLogger('audit')
    logger.info(message)