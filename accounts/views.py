from django.shortcuts import render
from django.http import HttpResponse
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

def createOrder(request):
    form = OrderForm(request)
    if request.method == 'POST':
        print('printing POST:',request.POST)
    form = OrderForm(request.POST)
    
    context={'form': form}
    return render(request,'accounts/order_form.html',context)