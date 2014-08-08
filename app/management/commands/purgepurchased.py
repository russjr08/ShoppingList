from django.core.management.base import BaseCommand, CommandError
from app.models import Item

class Command(BaseCommand):
    help = 'Automatically purges Items marked as Purchased'

    def handle(self, *args, **options):
        for item in Item.objects.all():
            if item.item_purchased is True:
                i = Item.objects.get(pk=item.pk)
                i.delete()
                self.stdout.write("Deleted Purchased Item: " + item.item_name)
