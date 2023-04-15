from django.db import models
from django.utils.translation import gettext_lazy as _

# TODO: nullability
class StaticCharField(models.CharField):
    def db_type(self, connection):
        varchar = super().db_type(connection)
        char = varchar.replace('varchar', 'char')
        return char

class Customer(models.Model):
    # Django automatically includes an autoincrementing `id` pk in every model.
    name = models.CharField(max_length=50)
    prime_user = models.BooleanField()
    # I don't think this should be in; it looks unnormalized
    # gift_card_balance = models.IntegerField()
    def get_or_make(**kwargs):
        try:
            return Customer.objects.get(**kwargs)
        except Customer.DoesNotExist:
            cust = Customer(**kwargs)
            cust.save()
            return cust

class Category(models.Model):
    description = models.CharField(max_length=100)
    def products(self): 
        return Product.objects.all().filter(category=self)
    
    def get_or_make(**kwargs):
        try:
            return Category.objects.get(**kwargs)
        except Category.DoesNotExist:
            cat = Category(**kwargs)
            cat.save()
            return cat

class Product(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT) # on_update defaults to RESTRICT
    # TODO: review decisions about on_update, on_delete
    list_price = models.DecimalField(max_digits=5, decimal_places=2)
    variants = models.ManyToManyField("self")
    def reviews(self):
        return Review.objects.all().filter(product=self)

    def get_or_make(**kwargs):
        try:
            return Product.objects.get(**kwargs)
        except Product.DoesNotExist:
            prod = Product(**kwargs)
            prod.save()
            return prod

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    product_id = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    def get_or_make(**kwargs):
        try:
            return Cart.objects.get(**kwargs)
        except Cart.DoesNotExist:
            cart = Cart(**kwargs)
            cart.save()
            return cart

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    shipping_address = models.CharField(max_length=50)

    def get_or_make(**kwargs):
        try:
            return Order.objects.get(**kwargs)
        except Order.DoesNotExist:
            ord = Order(**kwargs)
            ord.save()
            return ord

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=5, decimal_places=2)

    def get_or_make(**kwargs):
        try:
            return OrderDetail.objects.get(**kwargs)
        except OrderDetail.DoesNotExist:
            detail = OrderDetail(**kwargs)
            detail.save()
            return detail

class Rating(models.Model):
    code = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    def media(self):
        return Media.objects.all().filter(rating=self)
    def get_or_make(**kwargs):
        try:
            return Rating.objects.get(**kwargs)
        except Rating.DoesNotExist:
            rating = Rating(**kwargs)
            rating.save()
            return rating

class Media(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    rating = models.ForeignKey(Rating, on_delete=models.RESTRICT)
    def get_or_make(**kwargs):
        try:
            return Media.objects.get(**kwargs)
        except Media.DoesNotExist:
            media = Media(**kwargs)
            media.save()
            return media

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    stars = models.IntegerField()

class PaymentMethod(models.Model):
    class CardType(models.TextChoices):
        GIFT_CARD = "gift_card", _("Gift Card")
        CREDIT_CARD = "credit_card", _("Credit Card")
    
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    card_type = models.CharField(max_length=12, choices=CardType.choices)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    credit_card_number = StaticCharField(max_length=16)
    billing_address = models.CharField(max_length=50)

class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT)
    payment_quantity = models.DecimalField(max_digits=5, decimal_places=2)