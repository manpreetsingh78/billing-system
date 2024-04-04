from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Bill
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('item_list')  # Redirect to the desired page after login.
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})
@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form})
@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form})
@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item_confirm_delete.html', {'item': item})
@login_required
def generate_bill(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        items = Item.objects.filter(pk__in=item_ids)
        total_cost = sum(item.price for item in items)
        bill = Bill.objects.create(total_cost=total_cost)
        bill.items.set(items)
        return render(request, 'bill_detail.html', {'bill': bill})
    else:
        items = Item.objects.all()
    return render(request, 'generate_bill.html', {'items': items})
