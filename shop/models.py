from django.db import models
from django.contrib.auth.models import User


class MyCategory(models.Model):
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    category=models.ForeignKey(MyCategory,on_delete=models.CASCADE)
    description=models.TextField(max_length=1000,default="")
    img_link=models.CharField(max_length=1000,default="images/watch.png")
    inStock=models.BooleanField(default=True)
    final_price=models.FloatField(default=0.0)
    isInSale=models.BooleanField(default=False)
    isNew=models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WishList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

   
    def __str__(self):
        return f"{self.user.username}'s wishlist"
    
    @property 
    def get_cart_item_name(self):
        return self.product.name




class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    total=models.FloatField(default=0)
    final_total=models.FloatField(default=0)



    def __str__(self):
        return f"{self.user.username}'s cart"
    



class CartItem(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.FloatField()

    def __str__(self):
        return f"{self.product.name}"

    @property 
    def get_cart_item_name(self):
        return self.product.name
    
    @property 
    def get_cart_item_price(self):
        return self.product.price

    @property 
    def get_cart_user(self):
        return self.cart

ORDER_INFO = ( 
    ("PENDING", "PENDING"),
    ("ORDER READY", "ORDER READY"), 
    ("ON THE WAY", "ON THE WAY"), 
    ("DELIVERED", "DELIVERED"),  
) 
 

class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=200)
    paid=models.BooleanField(default=False)
    status=models.CharField(max_length=100,choices=ORDER_INFO,default="PENDING")
    phone=models.IntegerField()

    def __str__(self):
        return f"{self.cart}"


class OrderHistory(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.FloatField()

    def __str__(self):
        return f"{self.product.name}"

    @property 
    def get_cart_item_name(self):
        return self.product.name
    
    @property 
    def get_cart_item_price(self):
        return self.product.price

    @property 
    def get_cart_user(self):
        return self.cart


