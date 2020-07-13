# Generated by Django 3.0.8 on 2020-07-13 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('task_type', models.IntegerField(choices=[(1, 'image_only'), (2, 'classification')])),
                ('status', models.IntegerField(choices=[(1, 'completed'), (2, 'processing'), (3, 'error')])),
                ('created_at', models.DateTimeField(verbose_name='date published')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Project')),
                ('train_dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='train_dataset', to='main.Dataset')),
                ('val_dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='val_dataset', to='main.Dataset')),
            ],
        ),
    ]
