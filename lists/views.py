from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List 
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    form = ItemForm()
    context = {'form': form}
    return render(request, 'home.html', context)

def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text=request.POST['text'])
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            Item.objects.create(list=list_, text=request.POST['text'])
            return redirect(list_)
    context = {'list': list_, 'form': form}
    return render(request, 'view.html', context)

