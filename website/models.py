from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone

class Record(models.Model):
    #Basic Info
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    
    # fields for ML model
    contract = models.CharField(max_length=20, choices=[
        ('Month-to-month', 'Month-to-month'),
        ('One year', 'One year'),
        ('Two year', 'Two year')
    ], default = 'Month-to-month')  
    tenure = models.IntegerField(default=0)  
    monthly_charges = models.DecimalField(max_digits=10, decimal_places=2,default=0)  
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    payment_method = models.CharField(max_length=50, choices=[
        ('Electronic check', 'Electronic check'),
        ('Mailed check', 'Mailed check'),
        ('Bank transfer', 'Bank transfer'),
        ('Credit card', 'Credit card')
    ], default = "Credit Card")  
    internet_service = models.CharField(max_length=20, choices=[
        ('DSL', 'DSL'),
        ('Fiber optic', 'Fiber optic'),
        ('No', 'No')], default = "No")  
    online_security = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")
    online_backup = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")   
    tech_support = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")   
    paperless_billing = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No', 'No')], default = "No") 
    streaming_tv = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")   
    streaming_movies = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")

    phone_service = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No', 'No')], default = "No")
    device_protection = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')], default = "No")
    multiple_lines = models.CharField(max_length=20, choices=[
        ('Yes', 'Yes'),
        ('No phone service', 'No phone service'),
        ('No', 'No')], default = "No")
    
    
    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
    def to_dict(self):
        return {
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': str(self.phone),
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'contract': self.contract,
            'tenure': self.tenure,
            'monthly_charges': self.monthly_charges,
            'total_charges': self.total_charges,
            'payment_method': self.payment_method,
            'internet_service': self.internet_service,
            'online_security': self.online_security,
            'online_backup': self.online_backup,
            'tech_support': self.tech_support,
            'paperless_billing': self.paperless_billing,
            'streaming_tv': self.streaming_tv,
            'streaming_movies': self.streaming_movies,
            'phone_service':self.phone_service,
            'device_protection':self. device_protection,
            'multiple_lines':self.multiple_lines,
            'ID': self.id
        }
        
class Note(models.Model):
    customer = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices =[('Low','Low')
                                                         ,('Medium','Medium'),('High','High')], default='Low')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title
