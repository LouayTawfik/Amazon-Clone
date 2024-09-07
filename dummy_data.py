import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from product.models import Brand, Product

def seed_brand(n):
    fake = Faker()
    images = ['1.png', '2.png', '3.jpg', '4.png', '5.png', '6.jpg', '7.jpg', '8.png', '9.png']
    for _ in range(n):
        Brand.objects.create(
            name=fake.name(),
            image=f'brands/{images[random.randint(0, 8)]}'
        )
    print(f'Seed {n} brands successfully!')

def seed_product(n):
    fake = Faker()
    images = ['1.jpeg', '2.jpeg', '3.jpeg', '4.jpeg', '5.jpg', '6.jpg', '7.jpeg', '8.jpg', '9.jpg']
    flags = ['New', 'Sale', 'Feature']
    for _ in range(n):
        Product.objects.create(
            name=fake.name(),
            image=f'products/{images[random.randint(0, 8)]}',
            flag= flags[random.randint(0, 2)],
            price=round(random.uniform(20.99, 99.99), 2),
            sku=random.randint(1000, 10000000),
            subtitle=fake.text(max_nb_chars=250),
            description=fake.text(max_nb_chars=2000),
            quantity=random.randint(0, 30),
            brand=Brand.objects.get(id=random.randint(1, 5))
        )
    print(f'Seed {n} products successfully!')

# seed_brand(5)
seed_product(2000)