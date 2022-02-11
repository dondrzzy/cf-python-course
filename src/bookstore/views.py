from django.shortcuts import render, redirect  
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm

form = AuthenticationForm()


def login_view(request):                              
   error_message = None   
   form = AuthenticationForm()

   if request.method == 'POST':       
       form =AuthenticationForm(data=request.POST)

       if form.is_valid():                                
           username=form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')

           user=authenticate(username=username, password=password)
           if user is not None:
               login(request, user)                
               return redirect('sales:records')
       else:
           error_message ='ooops.. something went wrong'

   #prepare data to send from view to template
   context = {                                             
       'form': form,                                 #send the form data
       'error_message': error_message                     #and the error_message
   }
   #load the login page using "context" information
   return render(request, 'auth/login.html', context)


def logout_view(request):                                  
   logout(request)
   return redirect('login')
