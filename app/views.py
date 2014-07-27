import json
import datetime
from django.core import serializers

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
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


# API Requests

'''
Warning: Some of these API calls have not been documented. Why? The function names are pretty self explanatory.
'''

# /api/items/
def api_get_items(request):
    return HttpResponse(serializers.serialize('json', Item.objects.all()), content_type="application/json")


# /api/items/:id/
def api_get_single_item(request, item_id):
    get_object_or_404(Item, item_id)
    return HttpResponse(serializers.serialize('json', Item.objects.filter(pk=item_id)), content_type="application/json")


# /api/items/new/
'''
Adds a new item to the database, requires the following POST data:
name: The name of the item
author: Who added / requested the item
store: Where the item can be found

Optional POST data:
priority: Is the item a priority? (Can be either 'true', 'yes', 'false', or 'no'.)

If the request is made, an internal request to /api/items/:new_item_id/ will be called,
and the JSON data will be returned.

If an error is encountered, it will be returned and the request will not be processed/saved.
'''
@csrf_exempt
def api_add_new_item(request):
    if request.POST:
        if request.POST['name'] is None or request.POST['author'] is None or request.POST['store'] is None:
            return HttpResponse("Invalid request (You're missing a required field)", content_type="text/plain")

        i = Item()
        i.item_name = request.POST['name']
        i.item_author = request.POST['author']
        i.item_store = request.POST['store']

        if request.POST.get('priority', 'false') == 'true' or request.POST.get('priority', 'false') == 'yes':
            i.item_is_priority = True
        elif request.POST.get('priority', 'false') == 'false' or request.POST.get('priority', 'false') == 'no'\
                or request.POST.get('priority', 'false') is None:
            i.item_is_priority = False

        i.item_purchased = False
        i.item_date_added = datetime.datetime.today()

        i.save()

        print("API request (/api/items/new/) successfully processed. Handing off to api_get_single_item()")
        return api_get_single_item(request, i.pk)

    else:
        return HttpResponse("Invalid request (Missing POST data)", content_type="text/plain")


# /api/items/delete/:id/
def api_delete_item(request, item_id):
    # get_object_or_404(Item, item_id)

    json_data = serializers.serialize('json', Item.objects.filter(pk=item_id))
    Item.objects.filter(pk=item_id).delete()
    return HttpResponse(json_data, content_type="application/json")