from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from lists.forms import (
	ItemForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingListItemForm
	)
from lists.models import Item,List

def home_page(request):
	return render(request, 'home.html',{'form':ItemForm()})

def view_list(request,list_id):
	#We retrieve the list object from the URL
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)
	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(request, 'list.html',{'list':list_, 'form':form})

def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html',{"form":form})
	
	