import datetime
from django.db import models

# Create your models here.


class Item(models.Model):

    item_name = models.CharField("Name of Item", max_length=30)
    item_author = models.CharField("Whose requesting this?", max_length=30)

    item_store = models.CharField("What store can this be found from?", max_length=60)

    item_purchased = models.BooleanField("Item already purchased?", default=False)
    item_is_priority = models.BooleanField("Item is Urgent?", default=False)

    item_date_added = models.DateTimeField("Requested At", default=datetime.datetime.today())

    item_category = models.CharField("Category", max_length=20)

    def item_should_be_listed(self):
        if self.item_date_added >= datetime.datetime.today():
            return True
        elif self.item_date_added < datetime.datetime.today():
            return False

    def __unicode__(self):
        return "Item: " + self.item_name
