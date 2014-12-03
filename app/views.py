import json
import datetime
import os
from django.utils import timezone
from django.core import serializers
from django.core.urlresolvers import reverse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from app.models import Item
from ShoppingList.settings import BASE_DIR

# Static pages

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'available_items'

    def get_queryset(self):
        return Item.objects.all().order_by('item_category')

def BetaIndexView(request):
    if os.path.isfile(os.path.join(BASE_DIR, 'announce.txt')):

        return render(request, 'app/index.html', {
            'available_items': Item.objects.order_by('item_category'),
            'announcement': open(os.path.join(BASE_DIR, 'announce.txt'), 'r').read().rstrip()
        })
    else:
        return render(request, 'app/index.html', {
            'available_items': Item.objects.order_by('item_category')
        })

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

    if request.POST.get('priority', 'false') == 'true' or request.POST.get('priority', 'false') == 'yes' or request.POST.get('priority', 'false') == 'on':
            i.item_is_priority = True
    elif request.POST.get('priority', 'false') == 'false' or request.POST.get('priority', 'false') == 'no'\
            or request.POST.get('priority', 'false') is None:
        i.item_is_priority = False

    i.item_category = request.POST['category']

    i.item_purchased = False
    i.item_date_added = timezone.now()


    i.save()

    print("Request processed.")

    return HttpResponseRedirect(reverse('index'))


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
        if request.POST.get('name', None) is None:
            return HttpResponse("Invalid request (You're missing a required field)", content_type="text/plain")

        i = Item()
        i.item_name = request.POST.get('name', '')
        i.item_author = request.POST.get('author', '')
        i.item_store = request.POST.get('store', '')

        if request.POST.get('priority', 'false') == 'true' or request.POST.get('priority', 'false') == 'yes':
            i.item_is_priority = True
        elif request.POST.get('priority', 'false') == 'false' or request.POST.get('priority', 'false') == 'no'\
                or request.POST.get('priority', 'false') is None:
            i.item_is_priority = False

        i.item_category = request.POST['category']

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


# /api/items/categories/
def api_get_categories(request):
    categories = []
    items = Item.objects.all().order_by('item_category')
    for item in items:
        if not categories.__contains__(item.item_category):
            categories.append(item.item_category)

    return HttpResponse(json.dumps({'categories' : categories}), content_type="application/json")

# /api/items/modify/:id/
@csrf_exempt
def api_modify_item(request, item_id):
    item = Item.objects.get(pk=item_id)

    if request.POST.get('purchased', 'false') == 'true':
        item.item_purchased = True
    elif request.POST.get('purchased', 'false') == 'false':
        item.item_purchased = False

    if request.POST.get('priority', 'false') == 'true':
        item.item_is_priority = True
    elif request.POST.get('priority', 'false') == 'false':
        item.item_is_priority = False

    item.save()

    return HttpResponse(serializers.serialize('json', Item.objects.filter(pk=item_id)), content_type="application/json")


