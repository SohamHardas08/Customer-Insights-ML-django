# Generated by Django 5.1.2 on 2024-10-18 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='multiple_lines',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No phone service', 'No phone service'), ('No', 'No')], default='No', max_length=20),
        ),
    ]
