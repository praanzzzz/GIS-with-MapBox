from django.db import models

class FarmModel(models.Model):
    # Primary key field
    farm_id = models.AutoField(primary_key=True)
    barangay = models.CharField(max_length=255)
    city_or_municipality = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Philippines")
    acres = models.DecimalField(max_digits=10, decimal_places=2)
    crops_planted = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Farm ID: {self.farm_id}, {self.barangay}, {self.city_or_municipality}, {self.country}"

    @property
    def full_address(self):
        return f"{self.barangay}, {self.city_or_municipality}, {self.country}"
