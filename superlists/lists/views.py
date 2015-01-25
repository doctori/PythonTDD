from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from lists.models import Item,List
def home_page(request):
	return render(request, 'home.html')

def view_list(request,list_id):
	#We retrieve the list object from the URL
	list_ = List.objects.get(id=list_id)
	if request.method == 'POST':
		item=Item.objects.create(text=request.POST['item_text'],list=list_)
		try:
			item.full_clean()
			item.save()
			return redirect('/lists/%d/' % (list_.id,))
		except ValidationError:
			item.delete()
			error = 'Impossible d\'avoir un élement Vide'
			return render(request,'list.html', {'list':list_, 'error':error})
	return render(request, 'list.html',{'list':list_})

def new_list(request):
	list_ = List.objects.create()
	item=Item.objects.create(text=request.POST['item_text'],list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		item.delete()
		error = 'Impossible d\'avoir un élement Vide'
		return render(request, 'home.html',{"error":error})
	return redirect('/lists/%d/' % (list_.id,))
	
