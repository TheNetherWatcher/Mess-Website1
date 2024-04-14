from django.db import models
from .students import Student
from .caterer import Caterer
from .messperiod import messPeriod
import datetime

class shortRebate(models.Model):
    student_applied = models.ForeignKey(
        Student, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Student Email"
    )
    rebating_caterer = models.ForeignKey(
        Caterer,
        related_name="caterer",
        on_delete=models.SET_NULL,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    date_applied = models.DateField(default=datetime.date.today)
    amount = models.IntegerField(null=True)
    mess_period = models.ForeignKey(messPeriod, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.student_applied.name} | {self.start_date} to {self.end_date}"
    class Meta:
        verbose_name = "Short Rebate Details"
        verbose_name_plural = "Short Rebate Details"