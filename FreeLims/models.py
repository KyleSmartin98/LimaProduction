from django.db import models

class sample(models.Model):
    SAMPLE_TYPE = (
        ('Solid', 'Solid'),
        ('Liquid', 'Liquid'),
        ('Powder', 'Powder')
    )
    organization = models.CharField(max_length=200)
    sample_name = models.CharField(max_length=100)
    sample_description = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=100)
    sample_volume = models.CharField(max_length=100)
    sample_quantity = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=100, choices = SAMPLE_TYPE)
    expiration_date = models.CharField(max_length=100)
    logged_date = models.CharField(max_length=100)
    logged_by = models.CharField(max_length=100)

