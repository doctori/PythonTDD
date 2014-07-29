from django.shortcuts import render,redirect
from lists.models import Item,List
def home_page(request):
	items = Item.objects.all()
	return render(request, 'home.html',{'items':items})

def view_list(request,list_id):
	list_ = List.objects.get(id=list_id)
	return render(request, 'list.html',{'list':list_})

def new_list(request):
	list_ = List.objects.create()
	if len(request.POST['item_text']) > 0:
		Item.objects.create(text=request.POST['item_text'],list=list_)
	return redirect('/lists/%d/' % (list_.id,))
def add_item(request,list_id):
	list_ = List.objects.get(id=list_id)
	if len(request.POST['item_text']) > 0:
		Item.objects.create(text=request.POST['item_text'],list=list_)
	return redirect('/lists/%d/' % (list_.id,))