# Generated by Django 5.1.2 on 2024-10-18 05:58

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=20)),
                ('contract', models.CharField(choices=[('Month-to-month', 'Month-to-month'), ('One year', 'One year'), ('Two year', 'Two year')], default='Month-to-month', max_length=20)),
                ('tenure', models.IntegerField(default=0)),
                ('monthly_charges', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_charges', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Electronic check', 'Electronic check'), ('Mailed check', 'Mailed check'), ('Bank transfer', 'Bank transfer'), ('Credit card', 'Credit card')], default='Credit Card', max_length=50)),
                ('internet_service', models.CharField(choices=[('DSL', 'DSL'), ('Fiber optic', 'Fiber optic'), ('No', 'No')], default='No', max_length=20)),
                ('online_security', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
                ('tech_support', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
                ('paperless_billing', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=20)),
                ('streaming_tv', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
                ('streaming_movies', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
                ('phone_service', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=20)),
                ('device_protection', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
                ('multiple_lines', models.CharField(choices=[('Yes', 'Yes'), ('No internet service', 'No internet service'), ('No', 'No')], default='No', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='website.record')),
            ],
        ),
    ]