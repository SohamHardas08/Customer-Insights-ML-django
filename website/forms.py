from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Note
from django.utils import timezone
from django.core.exceptions import ValidationError

class Signup(UserCreationForm):
    #custom field
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 
                                                                     'placeholder': 'Email Address'})) #textbox, bootstrap class
    first_name = forms.CharField(label="", max_length=100,widget = forms.TextInput(attrs={'class':'form-control', 
                                                                     'placeholder': 'first name'}))
    last_name = forms.CharField(label="", max_length=100, widget = forms.TextInput(attrs={'class':'form-control', 
                                                                     'placeholder': 'last name'}))
    
    #Django defined fields
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(Signup,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control' #same as defined above
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ol class="form-text text-muted small "><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ol>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	
        
        


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
        label='First Name'
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
        label='Last Name'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
        label='Email'
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}),
        label='Phone'
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
        label='City'
    )
    state = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
        label='State'
    )
    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
        label='Zip Code'
    )
    contract = forms.ChoiceField(
        choices=[
            ('Month-to-month', 'Month-to-month'),
            ('One year', 'One year'),
            ('Two year', 'Two year'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Contract'
    )
    tenure = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Tenure', 'class': 'form-control'}),
        label='Tenure (in months)'
    )
    monthly_charges = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Monthly Charges', 'class': 'form-control'}),
        label='Monthly Charges'
    )
    total_charges = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Total Charges', 'class': 'form-control'}),
        label='Total Charges'
    )
    payment_method = forms.ChoiceField(
        required=True,
        choices=[
            ('Electronic check', 'Electronic check'),
            ('Mailed check', 'Mailed check'),
            ('Bank transfer', 'Bank transfer'),
            ('Credit card', 'Credit card'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Payment Method'
    )
    internet_service = forms.ChoiceField(
        required=True,
        choices=[
            ('DSL', 'DSL'),
            ('Fiber optic', 'Fiber optic'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Internet Service'
    )
    online_security = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No internet service', 'No internet service'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Online Security')
        
    online_backup = forms.ChoiceField(required=True, choices=[
        ('Yes', 'Yes'),
        ('No internet service', 'No internet service'),
        ('No', 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Online Backup')
    
    tech_support = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No internet service', 'No internet service'),
            ('No', 'No'),
        ],
       widget=forms.Select(attrs={'class': 'form-control'}),
       label='Tech Support'
    )
    paperless_billing = forms.ChoiceField(
        choices = [
            ('Yes', 'Yes'),
            ('No', 'No')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Paperless Billing'
    )
    streaming_tv = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No internet service', 'No internet service'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Streaming TV'
    )
    streaming_movies = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Streaming Movies'
    )
    
    phone_service = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Phone Service'
    )
     
    device_protection = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Device Protection'
    )
    
    multiple_lines = forms.ChoiceField(
        required=True,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Multiple Lines'
    )
    
    class Meta:
        model = Record
        exclude = ("user", )

class NoteForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':3,'class': 'form-control'})
    )
    deadline = forms.DateField(
        required=False,  
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control' ,'id':'deadline'}),
        input_formats = ['%Y-%m-%d']
    )
    priority = forms.ChoiceField(
        required=True,
        choices=[('Low','Low')
                ,('Medium','Medium'),('High','High')],
        widget=forms.Select(attrs={'class': 'form-control'})
    
    )
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'priority','deadline']
        