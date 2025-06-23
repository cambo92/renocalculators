from django.db import models

# Create your models here.
class Member(models.Model):
    perimeter = models.DecimalField(decimal_places=1, max_digits=5)
    height = models.DecimalField(decimal_places=1, max_digits=5)
    sq_per_litre = models.DecimalField(decimal_places=1, max_digits=5)
    num_coats = models.DecimalField(decimal_places=0, max_digits=1)
    cost_per_litre = models.DecimalField(decimal_places=2, max_digits=7)