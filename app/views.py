import json
import datetime
from django.core import serializers

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import generic
from app.models import Item


# Static pages

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'available_items'

    def get_queryset(self):
        return Item.objects.all()


def detail(request, item_id):
    i = get_object_or_404(Item, pk=item_id)

    return render(request, 'app/detail.html', {
        'item': i
    })

def new_item(request):
    return render(request, 'app/new.html')

def add_item(request):
    print("Request for new item is being processed...")
    print(request.POST['name'])
    print(request.POST['author'])
    print(request.POST['store'])


    i = Item()
    i.item_name = request.POST['name']
    i.item_author = request.POST['author']
    i.item_store = request.POST['store']
    if request.POST['priority']:
        i.item_is_priority = True
    else:
        i.item_is_priority = False

    i.item_purchased = False
    i.item_date_added = datetime.datetime.today()

    i.save()

    print("Request processed.")

    return render(request, 'app/index.html')
# API
def api_get_items(request):

    return HttpResponse(serializers.serialize('json', Item.objects.all()), content_type="application/json")
