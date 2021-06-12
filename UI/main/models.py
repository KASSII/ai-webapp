from django.db import models
import enum

# Enum Class
class TaskType(enum.Enum):
    classification = 0
    detection = 1
    segmentation = 2
    @classmethod
    def choices(cls):
        return [(m.value, m.name) for m in cls]

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    task_type = models.IntegerField(
        choices=TaskType.choices()
    )
    api_url = models.CharField(max_length=100)
    def __str__(self):
        return self.name