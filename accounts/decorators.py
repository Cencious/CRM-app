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

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrappper_func(request, *args, **kwargs):
            #set functionality to ensure a page is restricted 
            group = None
            if request.user.groups.exists():
                #set group value to first group in the list.
                group = request.user.groups.all()[0].name
                print('group: '+group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not autorised to view this page.')
        return wrappper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        return wrapper_function
