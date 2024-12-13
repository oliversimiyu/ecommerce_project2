from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Email verification fields
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.email
    
    def send_verification_email(self):
        verification_url = f"{settings.SITE_URL}{reverse('verify_email', kwargs={'token': self.email_verification_token})}"
        context = {
            'user': self,
            'verification_url': verification_url,
        }
        
        # Render email templates
        html_content = render_to_string('users/emails/verify_email.html', context)
        text_content = render_to_string('users/emails/verify_email.txt', context)
        
        # Create email
        subject = 'Verify your email address'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.email
        
        # Create message with both HTML and text versions
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        
        # Send email
        msg.send()
        
        # Update verification sent timestamp
        self.email_verification_sent_at = timezone.now()
        self.save(update_fields=['email_verification_sent_at'])
