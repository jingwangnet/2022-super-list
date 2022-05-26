from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List 
from lists.forms import ItemForm, ExistingListItemForm


User = get_user_model()

# Create your views here.
def home_page(request):
    form = ItemForm()
    context = {'form': form}
    return render(request, 'home.html', context)

def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

def view_list(request, pk):
    list_ = List.objects.get(pk=pk)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    context = {'list': list_, 'form': form}
    return render(request, 'view.html', context)


def my_list(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my.html', {'owner': owner})
