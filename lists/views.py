from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List 

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(list=list_, text=request.POST['new_item'])
    return redirect(f'/lists/{list_.pk}/')

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    context = {'list': list_}
    return render(request, 'view.html', context)

def add_item(request, pk):
    list_ = List.objects.get(pk=pk)
    item = Item.objects.create(list=list_, text=request.POST['new_item'])
    return redirect(f'/lists/{list_.pk}/')
