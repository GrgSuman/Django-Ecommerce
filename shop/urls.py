from django.urls import path
from .views import IndexView,AddToCartView,CartView,CheckoutView,RegistrationView,UserLoginView,UserLogoutView,ProductDetails,OrderTrackView,OrderCompleteView,AddToWishList,SearchView,CategoryPView


urlpatterns = [

    path("",IndexView.as_view(),name="index"),
    path("add/",AddToCartView.as_view(),name="add"),
    path("addTowishList/<int:id>",AddToWishList.as_view(),name="addWish"),
    path("details/<int:id>",ProductDetails.as_view(),name="more"),
    path("cart/",CartView.as_view(),name='cart'),
    path("checkout/",CheckoutView.as_view(),name='checkout'),
    path("register/",RegistrationView.as_view(),name='register'),
    path("login/",UserLoginView.as_view(),name='login'),
    path("logout/",UserLogoutView.as_view(),name='logout'),
    path("track-my-order/",OrderTrackView.as_view(),name='track'),
    path("order-completed/",OrderCompleteView.as_view(),name='order-complete'),
    path("search/",SearchView.as_view(),name="search"),
    path("product/",CategoryPView.as_view(),name="cate"),


]
