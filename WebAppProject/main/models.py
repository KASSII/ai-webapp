from django.db import models
from django.contrib.auth.models import User
import enum

# Enum Class
class TaskType(enum.Enum):
    image_only = 1
    classification = 2
    @classmethod
    def choices(cls):
        return [(m.value, m.name) for m in cls]

ReadDbType = {
    "with_label": ["classification"],
    "single_image": ["image_only"],
}

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField('date published')
    def __str__(self):
        return self.name

class Dataset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    task_type = models.IntegerField(
        choices=TaskType.choices()
    )
    created_at = models.DateTimeField('date published')
    def __str__(self):
        return self.name