import csv
import codecs

from django.shortcuts import render
from django.shortcuts import render

from bamazon.models import *
from bamazon.forms import *

def index(request):
    return render(request, "bamazon/index.html", {})

def categories(request):
    context = {"categories": Category.objects.all()}
    if request.method == "POST":
        import_categories(request)
    return render(request, "bamazon/categories.html", context)

def customers(request):
    context = {"customers": Customer.objects.all()}
    if request.method == "POST":
        import_customers(request)
    return render(request, "bamazon/customers.html", context)

def ratings(request):
    context = {"ratings": Rating.objects.all()}
    if request.method == "POST":
        import_ratings(request)
    return render(request, "bamazon/ratings.html", context)

def imports(request):
    context = {"form": ImportForm()}
    return render(request, "bamazon/import.html", context)

def import_categories(request):
    form = ImportForm(request.POST, request.FILES)
    file = request.FILES['import_file']
    reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        cat = Category.get_or_make(description=row[0])
        prod = Product.get_or_make(category=cat, name=row[1], description=row[2], list_price=row[3])

def import_customers(request):
    form = ImportForm(request.POST, request.FILES)
    file = request.FILES['import_file']
    reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        cust = Customer.get_or_make(name=row[0], prime_user=row[1].lower() == "true")
        ord = Order.get_or_make(customer=cust, shipping_address=row[2])
        prod = Product.get_or_make(name=row[3])
        detail = OrderDetail.get_or_make(order=ord, product=prod, quantity=row[4], cost=row[5])

def import_ratings(request):
    form = ImportForm(request.POST, request.FILES)
    file = request.FILES['import_file']
    reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        rating = Rating.get_or_make(code=row[0],full_name=row[1],description=row[2])
        media = Media.get_or_make(title=row[3],description=row[4],rating=rating)