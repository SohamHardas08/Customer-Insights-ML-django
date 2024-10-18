from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import Signup,AddRecordForm,NoteForm
from .models import Record, Note
import pandas as pd
import openpyxl
from django.views import View


def login_user(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['pass']
        #Authenticate
        user = authenticate(request, username = username, password = password)
        if user:
            login(request,user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.success(request, "Username/password incorrect")
            
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            form.save()
            #login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect(home)
        
    else:
            form = Signup()
            return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})



@login_required
def home(request):
    records = Record.objects.all()
    return render(request, 'home.html', {'records': records})

def records(request):
    records = Record.objects.all()
    data = [record.to_dict() for record in records]
    return JsonResponse(data, safe = False)

def export_data(request,format):
    records = Record.objects.all().values()
    df = pd.DataFrame.from_records(records)
    for column in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']):
        df[column] = df[column].dt.tz_localize(None)
    
    if format =='csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="records.csv"'
        df.to_csv(response, index=False)
        return response
    
    if format =='xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="records.xlsx"'
        df.to_excel(response, index=False, sheet_name='Customer_records')
        return response
    
    else:
        return HttpResponse(status = 400)
    
@login_required
def details(request, ID):
    customer_record = Record.objects.get(id = ID)
    return render(request, 'details.html', {'cust_rec': customer_record})


def delete_record(request, ID):
    if request.user.is_authenticated:
        del_record = Record.objects.get(id=ID)
        del_record.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('home')
    else:
        messages.error(request, 'Login to delete the record!')
        return redirect('login')

def update_record(request, ID):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = ID)
        form = AddRecordForm(request.POST or None, instance = current_record)
        if form.is_valid():
            form.save()
            messages.sucess('Record has been updated!')
            return redirect('home')
        
        return render(request, 'update_record.html',{'form' : form})
        
    
@login_required
def add_record(request):
   form = AddRecordForm(request.POST or None)
   if request.method == 'POST':
       if form.is_valid():
           add_record = form.save()
           messages.success(request, "Record added successfully!")
           return redirect('home')
    
   return render(request, 'add-record.html', {'form':form})


   
class NoteView(View):
    def get(self,request,ID, note_id = None):
        customer_record = Record.objects.get(id=ID)
        notes = Note.objects.filter(customer_id = ID, user = request.user)
        form = NoteForm()
        
        if note_id:
            note = Note.objects.get(id=note_id, user=request.user)
            form = NoteForm(instance=note)
            
            
        return render(request,'notes.html', {'notes': notes, 'form' : form ,'customer_record': customer_record ,'note_id' : note_id})
    
    def post(self,request,ID):
        form =  NoteForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                note = form.save(commit=False) #saves after user and customer_id are defined
                note.user = request.user
                note.customer_id = ID
                note.save()
                return redirect('notes', ID = ID) #ID is defined in the url route
        
        notes = Note.objects.filter(customer_id=ID, user=request.user)
        return render(request, 'notes.html', {'notes': notes, 'form': form, 'customer_id': ID})
    
    
def delete_note(request, ID, note_id):
    if request.user.is_authenticated:
        del_note = Note.objects.get(id = note_id)
        del_note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes', ID = ID)
    else:
        messages.error(request, 'Login to delete the note!')
        return redirect('login')
    
def edit_note(request, note_id, ID):
    if request.user.is_authenticated:
        current_note = Note.objects.get(id = note_id ,customer_id = ID, user= request.user)
        form = NoteForm(request.POST or None, instance = current_note)
        if form.is_valid():
            form.save()
            messages.success(request,'Note has been updated!')
            return redirect('notes', ID=ID)
        
        return render(request, 'notes.html',{'form' : form})
    else:
        return redirect('login')
