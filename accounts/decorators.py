from django.http import HttpResponse
from django.shortcuts import redirect


#stop unauthenticated user from accessing the login and register page.
#decorator is a function that takes in another function as apparator, allows adding an extra functionality before the original  function is called

def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func