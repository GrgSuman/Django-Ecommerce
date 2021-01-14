from django.contrib import admin
from .models import Product,Cart,CartItem,Order,OrderHistory,MyCategory,WishList


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price']

admin.site.register(Product,ProductAdmin)

admin.site.register(MyCategory)



class WishListAdmin(admin.ModelAdmin):
    list_display=['id','user','get_cart_item_name']

admin.site.register(WishList,WishListAdmin)






class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','total',"final_total"]

admin.site.register(Cart,CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','get_cart_item_name','get_cart_item_price',"quantity","subtotal","get_cart_user"]

admin.site.register(CartItem,CartItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','cart','phone',"address"]

admin.site.register(Order,OrderAdmin)

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display=['id','get_cart_item_name','get_cart_item_price',"quantity","subtotal","get_cart_user"]

admin.site.register(OrderHistory,OrderHistoryAdmin)