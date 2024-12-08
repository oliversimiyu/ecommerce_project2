from django.core.management.base import BaseCommand
from products.models import Category, Product
from django.core.files import File
from django.conf import settings
import os
import requests
from pathlib import Path
from django.utils.text import slugify
import tempfile

class Command(BaseCommand):
    help = 'Add sample products to the database'

    def download_image(self, url, product_name):
        try:
            # Create media directory if it doesn't exist
            media_root = settings.MEDIA_ROOT
            product_images_dir = os.path.join(media_root, 'products')
            os.makedirs(product_images_dir, exist_ok=True)

            # Download the image
            response = requests.get(url)
            if response.status_code == 200:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile()
                temp_file.write(response.content)
                temp_file.flush()

                # Create a filename
                file_name = f"{slugify(product_name)}.jpg"
                
                return File(temp_file, name=file_name)
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error downloading image for {product_name}: {str(e)}'))
            return None

    def handle(self, *args, **kwargs):
        # Sample products data with real image URLs
        products_data = {
            'Electronics': [
                {
                    'name': 'MacBook Pro 16"',
                    'description': 'Latest Apple MacBook Pro with M2 chip, 16GB RAM, 512GB SSD',
                    'price': 1999.99,
                    'stock': 50,
                    'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca4',
                    'brand': 'Apple',
                    'rating': 4.9,
                    'reviews_count': 452,
                    'express_delivery': True
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra',
                    'description': 'Latest Samsung flagship with 256GB storage, 12GB RAM',
                    'price': 1199.99,
                    'stock': 75,
                    'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf',
                    'brand': 'Samsung',
                    'rating': 4.7,
                    'reviews_count': 189,
                    'express_delivery': True
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'description': 'Premium noise-cancelling headphones with 30-hour battery life',
                    'price': 349.99,
                    'stock': 100,
                    'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
                    'brand': 'Sony',
                    'rating': 4.5,
                    'reviews_count': 328,
                    'express_delivery': False
                }
            ],
            'Fashion': [
                {
                    'name': 'Classic Leather Jacket',
                    'description': 'Genuine leather jacket with quilted lining',
                    'price': 199.99,
                    'stock': 30,
                    'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5',
                    'brand': "Levi's",
                    'rating': 4.6,
                    'reviews_count': 245,
                    'express_delivery': False
                },
                {
                    'name': 'Designer Sunglasses',
                    'description': 'UV-protected premium sunglasses with case',
                    'price': 149.99,
                    'stock': 45,
                    'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083',
                    'brand': 'Ray-Ban',
                    'rating': 4.4,
                    'reviews_count': 167,
                    'express_delivery': True
                },
                {
                    'name': 'Premium Watch',
                    'description': 'Stainless steel automatic watch with sapphire crystal',
                    'price': 499.99,
                    'stock': 25,
                    'image_url': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314',
                    'brand': 'Fossil',
                    'rating': 4.3,
                    'reviews_count': 89,
                    'express_delivery': False
                }
            ],
            'Home & Living': [
                {
                    'name': 'Smart LED TV 65"',
                    'description': '4K Ultra HD Smart TV with HDR',
                    'price': 899.99,
                    'stock': 20,
                    'image_url': 'https://images.unsplash.com/photo-1593784991095-a205069470b6',
                    'brand': 'Samsung',
                    'rating': 4.4,
                    'reviews_count': 167,
                    'express_delivery': True
                },
                {
                    'name': 'Robot Vacuum Cleaner',
                    'description': 'Smart robot vacuum with mapping technology',
                    'price': 299.99,
                    'stock': 40,
                    'image_url': 'https://images.unsplash.com/photo-1518640467707-6811f4a6ab73',
                    'brand': 'iRobot',
                    'rating': 4.3,
                    'reviews_count': 89,
                    'express_delivery': False
                },
                {
                    'name': 'Coffee Maker',
                    'description': 'Premium coffee maker with grinder',
                    'price': 199.99,
                    'stock': 35,
                    'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085',
                    'brand': 'Philips',
                    'rating': 4.5,
                    'reviews_count': 328,
                    'express_delivery': False
                }
            ],
            'Sports': [
                {
                    'name': 'Mountain Bike',
                    'description': 'Professional mountain bike with 21 speeds',
                    'price': 799.99,
                    'stock': 15,
                    'image_url': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91',
                    'brand': 'Trek',
                    'rating': 4.6,
                    'reviews_count': 245,
                    'express_delivery': False
                },
                {
                    'name': 'Tennis Racket Pro',
                    'description': 'Professional grade tennis racket',
                    'price': 159.99,
                    'stock': 30,
                    'image_url': 'https://images.unsplash.com/photo-1617083934555-ac7b4d0c8be2',
                    'brand': 'Wilson',
                    'rating': 4.4,
                    'reviews_count': 167,
                    'express_delivery': True
                },
                {
                    'name': 'Yoga Set',
                    'description': 'Complete yoga set with mat, blocks, and strap',
                    'price': 79.99,
                    'stock': 50,
                    'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b',
                    'brand': 'Lululemon',
                    'rating': 4.3,
                    'reviews_count': 89,
                    'express_delivery': False
                }
            ]
        }

        # Create products for each category
        for category_name, products in products_data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )
            
            for product_data in products:
                # Download image
                image_file = self.download_image(product_data['image_url'], product_data['name'])
                
                # Create or update product
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'category': category,
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'stock': product_data['stock'],
                        'brand': product_data['brand'],
                        'rating': product_data['rating'],
                        'reviews_count': product_data['reviews_count'],
                        'express_delivery': product_data['express_delivery'],
                        'slug': slugify(product_data['name'])
                    }
                )

                if image_file:
                    product.image.save(image_file.name, image_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'Added image for product "{product.name}"'))
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created product "{product.name}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product "{product.name}" already exists'))
