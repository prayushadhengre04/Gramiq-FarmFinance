from django.db import models
from django.utils import timezone


class FarmReport(models.Model):
    SEASON_CHOICES = [
        ('Kharif', 'Kharif'),
        ('Rabi', 'Rabi'),
        ('Zaid', 'Zaid'),
    ]

    farmer_name = models.CharField(max_length=100)
    crop_name = models.CharField(max_length=100)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    total_acres = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total area in acres")
    date_of_sowing = models.DateField()
    date_of_harvest = models.DateField()
    location = models.CharField(max_length=255, help_text="Village/Taluka/District/State")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer_name} - {self.crop_name} ({self.season})"


class Expense(models.Model):
    report = models.ForeignKey(FarmReport, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)


class Income(models.Model):
    report = models.ForeignKey(FarmReport, on_delete=models.CASCADE, related_name='incomes')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
