from django.db import models
import uuid
from django.contrib.auth.models import User

class ChangeRequest(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    ticket_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    employee_name = models.CharField(
        max_length=100
    )

    project_name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    attachment = models.FileField(
        upload_to='uploads/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = "CR-" + str(uuid.uuid4())[:8]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_number
    
class DeveloperAssignment(models.Model):

    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    change_request = models.OneToOneField(
        ChangeRequest,
        on_delete=models.CASCADE,
        related_name='assignment'
    )

    developer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Assigned'
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.change_request.ticket_number} - {self.developer.username}"