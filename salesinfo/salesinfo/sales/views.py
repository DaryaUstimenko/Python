
from .models import Customer, Seller, Product, Sale
from django.shortcuts import render, redirect
from .forms import CustomerForm, SellerForm, ProductForm, SaleForm
# Представление для отображения покупателей
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

# Представление для отображения продавцов
def seller_list(request):
    sellers = Seller.objects.all()
    return render(request, 'sales/seller_list.html', {'sellers': sellers})

# Представление для отображения товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

# Представление для отображения продаж
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})


# Представление для добавления покупателя
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/customer_form.html', {'form': form})

# Представление для добавления продавца
def seller_create(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller_list')
    else:
        form = SellerForm()
    return render(request, 'sales/seller_form.html', {'form': form})

# Представление для добавления товара
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'sales/product_form.html', {'form': form})

# Представление для добавления продажи
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/sale_form.html', {'form': form})
