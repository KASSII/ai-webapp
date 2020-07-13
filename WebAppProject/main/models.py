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

# Enum Class
class ProcessStatus(enum.Enum):
    completed = 1
    processing = 2
    error = 3

    @classmethod
    def choices(cls):
        return [(m.value, m.name) for m in cls]

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

class TrainLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    train_dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, related_name = "train_dataset")
    val_dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, related_name = "val_dataset")
    task_type = models.IntegerField(
        choices=TaskType.choices()
    )
    status = models.IntegerField(
        choices=ProcessStatus.choices()
    )
    created_at = models.DateTimeField('date published')
    def __str__(self):
        return self.description
