# Generated by Django 5.1.2 on 2024-10-20 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_note_deadline_note_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=10),
        ),
    ]
