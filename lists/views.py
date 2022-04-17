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
    items = Item.objects.filter(list=list_)
    context = {'items': items}
    return render(request, 'view.html', context)
