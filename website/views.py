from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import Signup, AddRecordForm, NoteForm
from .models import Record, Note
from .pre_processing import *
from datetime import datetime



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
            messages.success(request, 'Record has been updated!')
            return redirect('details', ID=ID)
        
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
        
        # deadline progress bar
        now = datetime.now().date()
        deadline_pcts = []
        for note in notes:
            
            created_at = note.created_at.date()
            if note.deadline:
                total_days = (note.deadline- created_at).days
                days_remaining = (note.deadline - now).days
            
                if days_remaining <=0:
                    percentage = 100
                else:
                    if total_days > 0:
                        percentage = ((total_days - days_remaining) / total_days) *100
                    else:
                        percentage = 100
            else:
                percentage=0
            deadline_pcts.append((note.id, percentage))
            
        form = NoteForm()
        
        if note_id:
            note = Note.objects.get(id=note_id, user=request.user)
            form = NoteForm(instance=note)
            
            
        return render(request,'notes.html', {'notes': notes, 'form' : form ,'customer_record': customer_record ,
                             'note_id' : note_id, 'deadline_pcts': deadline_pcts})
    
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
    
    def delete(request, ID, note_id):
        if request.user.is_authenticated:
            del_note = Note.objects.get(id = note_id)
            del_note.delete()
            messages.success(request, 'Note deleted successfully!')
            return redirect('notes', ID = ID)
        else:
            messages.error(request, 'Login to delete the note!')
        return redirect('login')
    
    def put(request, ID, note_id):
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
    
    

        
# prediction logic

class PredictChurnAPIView(APIView):
    def post(self, request, ID):
        try:
            customer = Record.objects.get(id=ID)
            prediction, probability = get_predictions(customer)
            
            return Response({
                'status': 'success',
                'customer_id': ID,
                'prediction': prediction,
                'probability': int(probability)
            }, status=status.HTTP_200_OK)
        
        except Record.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
     
    # testing the API view        
    def get(self,request, ID):
        try:
            customer = Record.objects.get(id=ID)
            return Response({
                'status': 'success',
                'customer_id':customer.id,
                'first_name':customer.first_name,
                'last_name':customer.last_name 
            }, status = status.HTTP_200_OK)
        except Record.DoesNotExist:
            return Response({
                'status' : 'error',
                'msg' : 'customer not found'
            }, status = status.HTTP_404_NOT_FOUND)
            
   
        

