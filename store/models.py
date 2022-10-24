from email.policy import default
from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # related_name='+' to solve the name clash
    # https://codewithmosh.com/courses/1422300/lectures/33213978
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)
    # below is how to set one to many relationship (collection can have multiple products)
    # PROTECT means, even if you accidentally delete collection, you don't delete product
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # many to many relationship
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    # since its a constant value, use uppercase
    # list of tuples below
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)  # choices


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # one to many: Oder can have multiple OrderItems
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    # one to many: Product can have multiple OrderItems
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# relationship: one to one with customer
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # below is how to set one to one relationship
    # CASCADE means, once customer is deleted, then address also will be deleted
    # primary_key=True protects as one to one relationship. if false, django will create an id to address,
    # then it ends up one to many relationship
    # Note: you don't need to create reverse relationship in the Customer class, since django will automatically create it for us
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)


class Cart(models.Model):
    # auto_now_add=True: date gets auto created when cart is created
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # one to many: Cart can have multiple CartItems
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # one to many: Product can have multiple CartItems
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()