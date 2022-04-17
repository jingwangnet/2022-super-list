from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['new_item'])
        return redirect('/')

    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'home.html', context)
