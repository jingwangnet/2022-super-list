from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List 

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    item = Item(list=list_, text=request.POST['new_item'])
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty item"
        return render(request, 'home.html', {'error': error})
    return redirect(list_)

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    error = None

    if request.method == 'POST':
        list_ = List.objects.get(pk=pk)
        try:
            item = Item(list=list_, text=request.POST['new_item'])
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty item"

    context = {'list': list_, 'error': error}
    return render(request, 'view.html', context)

