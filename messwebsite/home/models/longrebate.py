from django.db import models
from .students import Student
import datetime

class longRebate(models.Model):
    email = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True
    )
    start_date = models.DateField(
        null=True, 
        blank=True
    )
    end_date = models.DateField(
        null=True, 
        blank=True
    )   
    days = models.IntegerField(
        default=8
    )
    approved = models.BooleanField(
        default=False
    )
    
    REASON_TYPE_CHOICES = (
        ('', 'Choose the reason'),
        ('Incomplete form', 'Incomplete form'),
        ('There is a date mismatch between the one written in the form and the one in the attached form', 'There is a date mismatch between the one written in the form and the one in the attached form'),

    )
    reason = models.TextField(
        choices=REASON_TYPE_CHOICES, 
        default="",
        blank=True
    )
    date_applied = models.DateField(
        default=datetime.date.today
    )
    file = models.FileField(upload_to="documents/", default=None, null=True, blank=True)

    def __str__(self):
        return str(self.date_applied) +" "+ str(self.email)

    class Meta:
        verbose_name = "Long Rebate Details"
        verbose_name_plural = "Long Rebate Details"