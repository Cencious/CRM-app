from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm

# Create your views here.
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

def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{'products':products})

def customer(request, pk):
    customers = Customer.objects.get(id=pk) 

    orders= customers.order_set.all()
    order_count = orders.count()

    context={'customers': customers, 'orders': orders, 'order_count': order_count}
    return render(request,'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet =inlineformset_factory(Customer, Order, fields= ('products', 'status'))
    customers = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customers)
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

def deleteOrder(request, pk):#pass in a pk to delete a specific order
    #pass in item into the view
    order =Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context= {'item': order}
    return render(request,'accounts/delete.html',context)

