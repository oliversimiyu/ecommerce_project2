from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Setup initial test data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            'Electronics',
            'Books',
            'Clothing',
            'Home & Garden',
            'Sports & Outdoors'
        ]
        
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
            self.stdout.write(self.style.SUCCESS(f'Created category "{cat_name}"'))
