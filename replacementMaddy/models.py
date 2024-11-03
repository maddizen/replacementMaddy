from django.db import models
from django.contrib.auth.models import User

class ProjectQuotation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area_size = models.FloatField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    global_markup = models.FloatField(default=0.0)

    def total_cost(self):
        # Calculate total cost based on associated materials and markup
        total = sum(material.total_price() for material in self.projectmaterial_set.all())
        return total * (1 + self.global_markup / 100)

class ProjectElement(models.Model):
    name = models.CharField(max_length=255)

class Material(models.Model):
    name = models.CharField(max_length=255)
    base_price = models.FloatField()
    markup = models.FloatField(default=0.0)

    def total_price(self):
        return self.base_price * (1 + self.markup / 100)

class ProjectMaterial(models.Model):
    project = models.ForeignKey(ProjectQuotation, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def total_price(self):
        return self.material.total_price() * self.quantity