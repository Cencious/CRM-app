from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users,admin_only 

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@unauthenticated_user
def registerPage(request):
    
    form =CreateUserForm()

    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')

            #query the group to associate a user to customer
            group = Group.objects.get(name='Customer')
            user.groups.add(group)


            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
    context ={'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request,'Username OR password is incorrect')
                

    context ={}
    return render(request, 'accounts/login.html', context)

def logoutUser(request): 
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers =customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 
    'pending':pending,
    'delivered':delivered,'total_orders':total_orders}

    return render(request,'accounts/dashboard.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def userPage(request):
    context={}
    return render(request,'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(products,3)
    try:
        products = paginator.page(page)
    except PageNotAnInteger: 
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,'accounts/products.html',{'products':products, 'page':page})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk) 

    orders= customers.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders= myfilter.qs
    context={'customers': customers, 'orders': orders, 'order_count': order_count, 'myfilter': myfilter}
    return render(request,'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def createOrder(request, pk):
    OrderFormSet =inlineformset_factory(Customer, Order, fields= ('products', 'status'), extra=10)
    customers = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customers)
    # form = OrderForminitial=({'customers':customers})
    if request.method == 'POST':
        # print('printing POST:',request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customers)
        if formset.is_valid():
            formset.save()
          
            return redirect('/')

    
    context={'formset': formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def updateOrder(request, pk):
    order =Order.objects.get(id=pk) #to prefil the form, query item from here.
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) 
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form': form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteOrder(request, pk):#pass in a pk to delete a specific order
    #pass in item into the view
    order =Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context= {'item': order}
    return render(request,'accounts/delete.html',context)

