from django.db import models
# Create your models here.

class PlanningData(models.Model):

    location = models.CharField(max_length=200)

    estimated_cost = models.CharField(max_length=200)

    soil_information = models.TextField()

    required_permissions = models.TextField()

    def __str__(self):
        return self.location

from django.db import models


class PlanningData(models.Model):

    location = models.CharField(max_length=200)

    estimated_cost = models.CharField(max_length=200)

    soil_information = models.TextField()

    required_permissions = models.TextField()

    def __str__(self):
        return self.location
    
class ConstructionProgress(models.Model):

    project_stage = models.CharField(max_length=200)

    current_status = models.CharField(max_length=200)

    progress = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_stage} - {self.progress}%"

class CrackDetection(models.Model):

    image = models.ImageField(upload_to="crack_images/")

    result = models.CharField(max_length=200)

    confidence = models.FloatField(default=0)

    crack_count = models.IntegerField(default=0)

    severity = models.CharField(max_length=100)

    recommendation = models.TextField()

    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} - {self.confidence}%"

class MonitoringData(models.Model):

    project_stage = models.CharField(max_length=100)

    current_status = models.CharField(max_length=200)

    progress = models.IntegerField(default=0)

    planning_completed = models.BooleanField(default=True)

    site_preparation_completed = models.BooleanField(default=False)

    foundation_in_progress = models.BooleanField(default=False)

    structural_work_completed = models.BooleanField(default=False)

    final_inspection_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.project_stage    