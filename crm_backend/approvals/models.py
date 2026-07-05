from django.db import models
from tickets.models import ChangeRequest


class Approval(models.Model):

    LEVEL_CHOICES = (
        (1, "Level 1"),
        (2, "Level 2"),
    )

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    ticket = models.ForeignKey(
        ChangeRequest,
        on_delete=models.CASCADE,
        related_name="approvals"
    )

    level = models.IntegerField(choices=LEVEL_CHOICES)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(blank=True)

    approved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.ticket_number} - Level {self.level}"