from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Order,Cart,CartItem,Order,OrderHistory,WishList,MyCategory
from django.http import HttpResponse,JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import OrderForm
from django.contrib import messages
from random import randint
from django.http import JsonResponse
from django.views.generic import ListView
from django.db.models import Q
from itertools import chain


class IndexView(View):

    def get(self,request):
        if request.user.is_authenticated:
            arr=[]
            cart=Cart.objects.get(user=request.user.id)
            cartItems=cart.cartitem_set.all()
            for i in range(8):
                x=randint(1,26)
                pro=Product.objects.get(id=x)
                if pro in arr:
                    pass
                else:
                    arr.append(pro)
            watchs=Product.objects.filter(category__category="Smartphones")
            headphones=Product.objects.filter(category__category="Headphones")
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
            context={"wishLen":wishLen,"wishProducts":wishProducts,'products':Product.objects.all(),"cart":len(cartItems),"random":arr,"watchs":watchs,"headphones":headphones}
            return render(request,"index.html",context)
        else:
            wishLen=0
            wishProducts=[]
            arr=[]
            for i in range(8):
                x=randint(1,26)
                pro=Product.objects.get(id=x)
                if pro in arr:
                    pass
                else:
                    arr.append(pro)
            watchs=Product.objects.filter(category__category="Smartphones")
            headphones=Product.objects.filter(category__category="Headphones")
            context={"wishLen":wishLen,"wishProducts":wishProducts,'products':Product.objects.all(),"cart":0,"random":arr,"watchs":watchs,"headphones":headphones}
            return render(request,"index.html",context)

class ProductDetails(View):

    def get(self,request,id):
        if request.user.is_authenticated:
            product=Product.objects.get(id=id)
            category=product.category
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
            arr=[]
            for i in range(8):
                x=randint(1,26)
                pro=Product.objects.get(id=x)
                if len(arr)>5:
                    break
                else:
                    if pro in arr:
                        pass
                    else:
                        arr.append(pro)
            cart=Cart.objects.get(user=request.user.id)
            cartItems=cart.cartitem_set.all()
            context={"wishLen":wishLen,"wishProducts":wishProducts,"product":product,'cart':len(cartItems),"related":arr}
            return render(request,"product_details.html",context)
        else:

            product=Product.objects.get(id=id)
           
            wishLen=0
            wishProducts=[]
            arr=[]
            for i in range(8):
                x=randint(1,26)
                pro=Product.objects.get(id=x)
                if len(arr)>5:
                    break
                else:
                    if pro in arr:
                        pass
                    else:
                        arr.append(pro)
            context={"wishLen":wishLen,"wishProducts":wishProducts,"product":product,'cart':0,"related":arr}
            return render(request,"product_details.html",context)

class AddToWishList(View):
    def get(self,request,id):
        print("requested")
        if request.user.is_authenticated:
           product=Product.objects.get(id=id)
           isInList=WishList.objects.filter(product=id).filter(user=request.user)
           if isInList.exists():
               if request.GET.get("rem")=="1":
                   isInListItem=WishList.objects.filter(user=request.user).filter(product=id)
                   isInList[0].delete()
                   messages.success(request,"Removed from wishlist")
                   return redirect('index')
               else:
                   messages.success(request,"Already in WishList")
                   return redirect('index')

           else:
                WishList.objects.create(user=request.user,product=product)
                messages.success(request,"Successfully added in WishList")
                return redirect("index")

        else:
            return redirect("index")


class AddToCartView(View):
        def get(self,request):
            msg=""
            qty=0
            sub=0
            id=request.GET.get("id")
            id=int(id)
            product=Product.objects.get(id=id)

            if self.request.user.is_authenticated:

                cart=Cart.objects.get(user=request.user.id)                
                cartItems=cart.cartitem_set.all()

                if cartItems.exists():
                    isProductAlreadyInCart = cartItems.filter(product=id)
                    if isProductAlreadyInCart.exists():
                        inCart=cartItems.get(product=id)
                        if request.GET.get("dec")=="1":
                            if inCart.quantity==5:
                                msg="Max order limit is 5"
                                qty=5
                                sub=inCart.subtotal
                            else:
                                inCart.quantity +=1
                                inCart.subtotal =inCart.quantity*product.price
                                inCart.save()
                                qty=inCart.quantity
                                sub=inCart.subtotal

                        elif request.GET.get("dec")=="0":
                            if inCart.quantity==1:
                                msg="Order cannot be less than 1"
                                qty=1
                                sub=product.price
                            else:
                                inCart.quantity -=1
                                inCart.subtotal =inCart.quantity*product.price
                                inCart.save()
                                qty=inCart.quantity
                                sub=inCart.subtotal

                        
                        elif request.GET.get("dec")=="-":
                            inCart.delete()
                            msg="Item was removed from Cart."

                        else:
                            msg="Item was already added in Cart."
                    
                    else:
                        try:
                            order=Order.objects.get(cart=cart)
                            msg='To make a new Order your previous order must be completed.'
                        except:
                            CartItem.objects.create(cart=cart,product=product,quantity=1,subtotal=product.price)
                            msg='Item added successfully in cart.'

                    total=0;
                    for p in cartItems:
                        total=total+p.subtotal
                    cart.total=total
                    cart.save()

                else:
                    CartItem.objects.create(cart=cart,product=product,quantity=1,subtotal=product.price)
                    msg='Item added successfully in cart.'


                    total=0;
                    for p in cartItems:
                        total=total+p.subtotal
                    cart.total=total
                    cart.save()

                cart_items_length=len(cartItems)
                return JsonResponse({"size":cart_items_length,"total":total,"msg":msg,"qty":qty,"subtotal":f"Rs. {sub}"})
            

                        
#IF NOT LOGGED IN
            else:
                return JsonResponse({"size":0,"total":0,"msg":"","qty":0})

                # return redirect("login")


class CartView(View):

     def get(self,request):
        if request.user.is_authenticated:
            cart=Cart.objects.get(user=request.user)
            order=Order.objects.filter(cart=cart)
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
            if order.exists():
                return redirect("track")
            else:
                cart=Cart.objects.get(user=request.user.id)
                cartItems=cart.cartitem_set.all()
                context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems}
                return render(request,"cart.html",context)
            
        else:
            wishLen=0
            wishProducts=[]
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":0}
            return render(request,"cart.html",context)

       
class CheckoutView(View):

    def post(self,request):
        if request.user.is_authenticated:
            address=request.POST['address']
            phone=request.POST['phone']
            cart=Cart.objects.get(user=request.user)
            if len(phone)>8 and address!="":
                Order.objects.create(cart=cart,address=address,phone=phone)
                return redirect("index")

            else:
                cart=Cart.objects.get(user=request.user)
                order=Order.objects.filter(cart=cart)
                if order.exists():
                    return redirect("track")
                    
                else:
                    return redirect('checkout')

        
        else:
            return redirect("index")

           


    def get(self,request):

        if request.user.is_authenticated:
            order_fm=OrderForm()
            cart=Cart.objects.get(user=request.user.id)
            cartItems=cart.cartitem_set.all()
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"form":order_fm}
            return render(request,"order.html",context)
            
        else:
            return redirect("index")

           

class RegistrationView(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            fm=UserCreationForm()
            context={"cart":0,'form':fm}
            return render(request,"registration.html",context)


    def post(self,request):
        fm=UserCreationForm(request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            passw=fm.cleaned_data['password1']
            fm.save()
            user=User.objects.get(username=uname)
            Cart.objects.create(user=user)
            usr=authenticate(username=uname,password=passw)
            if usr is not None:
                login(request,usr)
                cart=Cart.objects.get(user=request.user)
                        
        return redirect("index")




class UserLoginView(View):
    def get(self,request):
        return redirect("index")


    def post(self,request):
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            passw=fm.cleaned_data['password']
            usr=authenticate(username=uname,password=passw)
            if usr is not None:
                login(request,usr)
                cart=Cart.objects.get(user=request.user)
                return redirect('index')
        else:
            return redirect('index')

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('index')

class OrderTrackView(View):
    def get(self,request):
        if request.user.is_authenticated:
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
            cart=Cart.objects.get(user=request.user)
            order=Order.objects.filter(cart=cart)
            orderHistory=OrderHistory.objects.filter(cart=cart)
            if order.exists():
                if orderHistory.exists():
                    cart=Cart.objects.get(user=request.user.id)
                    cartItems=cart.cartitem_set.all()
                    context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"order":order[0],"history":orderHistory,"h_len":len(orderHistory)}
                    return render(request,"track.html",context)
                else:
                    cart=Cart.objects.get(user=request.user.id)
                    cartItems=cart.cartitem_set.all()
                    context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"order":order[0],"history":[],"h_len":0}
                    return render(request,"track.html",context)
            else:
                 if orderHistory.exists():
                    cart=Cart.objects.get(user=request.user.id)
                    cartItems=cart.cartitem_set.all()
                    context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"history":orderHistory,"h_len":len(orderHistory)}
                    return render(request,"track.html",context)
                 else:
                    cart=Cart.objects.get(user=request.user.id)
                    cartItems=cart.cartitem_set.all()
                    context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"history":[],"cartItem":cartItems,"h_len":0}
                    return render(request,"track.html",context)
        else:
            return redirect('login')

class OrderCompleteView(View):
    def get(self,request):
        if request.user.is_authenticated:
            cart=Cart.objects.get(user=request.user)
            order=Order.objects.filter(cart=cart)
            if order.exists():
                cartItems=cart.cartitem_set.all()
                for cartItem in cartItems:
                    OrderHistory.objects.create(cart=cart,product=cartItem.product,quantity=cartItem.quantity,subtotal=cartItem.subtotal)
                cart.cartitem_set.all().delete()
                Order.objects.get(cart=cart).delete()
                cart.total=0
                cart.save()
                
                
                return redirect('index')
            else:
                return redirect('index') 
        else:
            return redirect("index")

class SearchView(ListView):

    def get(self,request):
        if request.user.is_authenticated:
            cart=Cart.objects.get(user=request.user)
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
        
            cart=Cart.objects.get(user=request.user.id)
            cartItems=cart.cartitem_set.all()
            qset=Product.objects.filter(Q(description__icontains=self.request.GET['q']) | Q(name__icontains=self.request.GET['q']))
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"object_list":qset}
            return render(request,"search.html",context)
            
        else:
            wishLen=0
            wishProducts=[]
            qset=Product.objects.filter(Q(description__icontains=self.request.GET['q']) | Q(name__icontains=self.request.GET['q']))
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":0,"object_list":qset}
            return render(request,"search.html",context)


class CategoryPView(ListView):

    def get(self,request):
        if request.user.is_authenticated:
            cart=Cart.objects.get(user=request.user)
            wish=WishList.objects.filter(user=request.user)
            if wish.exists():
                wishLen=len(wish)
                wishProducts=wish
            else:
                wishLen=0
                wishProducts=[]
        
            cart=Cart.objects.get(user=request.user.id)
            cartItems=cart.cartitem_set.all()
            cat=MyCategory.objects.get(category=self.request.GET['category'])
            product=Product.objects.all()
            qset=cat.product_set.all()
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":len(cartItems),"total":cart.total,"cartItem":cartItems,"object_list":qset}
            return render(request,"cat_products.html",context)
            
        else:
            wishLen=0
            wishProducts=[]
            cat=MyCategory.objects.get(category=self.request.GET['category'])
            product=Product.objects.all()
            qset=cat.product_set.all()
            context={"wishLen":wishLen,"wishProducts":wishProducts,"cart":0,"object_list":qset}
            return render(request,"cat_products.html",context)





