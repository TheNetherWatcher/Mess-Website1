from django.db import models

class messPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def month(self):
        return self.start_date.month

    def __str__(self):
        return f"{self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = "Mess Period"
        verbose_name_plural = "Mess Periods"