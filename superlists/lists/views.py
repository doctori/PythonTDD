from django.shortcuts import render,redirect
from lists.models import Item,List
def home_page(request):
	items = Item.objects.all()
	return render(request, 'home.html',{'items':items})

def view_list(request,list_id):
	items = Item.objects.all()
	return render(request, 'list.html',{'items':items})

def new_list(request):
	if len(request.POST['item_text']) > 0:
		list_ = List.objects.create()
		Item.objects.create(text=request.POST['item_text'],list=list_)
	return redirect('/lists/unique-list-name/')
	