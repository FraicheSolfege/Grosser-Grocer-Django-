from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    description = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.name

def create_product(name, image, description,  price):
    product = Product.objects.create(name=name, image=image, description=description, price=price)
    return product

def filter_product_by_id(id):
    product = Product.objects.get(id=id)
    return product

def get_all_products():
    products = Product.objects.all()
    return products

def update_product(id, new_name, new_description, new_price):
    product = Product.objects.get(id=id)
    product.name = new_name
    product.price = new_price
    product.description = new_description
    product.save()
    return product

def delete_product(id):
    product = Product.objects.get(id=id)
    product.delete()


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name

def create_order(customer, product, quantity, status):
    order = Order.objects.create(customer=customer, product=product, quantity = quantity, status=status)
    return order

def filter_order_by_id(id):
    order = Order.objects.get(id=id)
    return order

def get_all_orders():
    orders = Order.objects.all()
    return orders

def update_order(id, customer, product, quantity, status):
    order = Order.objects.get(id=id)
    order.customer = customer
    order.product = product
    order.quantity = quantity
    order.status = status
    order.save()
    return order

def delete_order(id):
    order = Order.objects.get(id=id)
    order.delete()