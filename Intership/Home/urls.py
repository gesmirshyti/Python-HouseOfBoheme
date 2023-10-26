from django.urls import path ,include
from . import views 
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('event', views.event, name='event'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    # path('addtocart/', views.add_to_cart,name='addtocart'),
    # path('pluscart/', views.plus_cart),
    # path('minuscart/', views.minus_cart),
    # path('removecart/', views.remove_cart),
    # path('cart/', views.show_cart, name='showcart'),
    path('checkout', views.checkout, name='checkout'),
    path('products', views.products, name='products'),
    path('Product_Detail/<id>', views.Product_Detail, name='Product_Detail'),
    path('article', views.articles, name='article'),
    path('article_Detail/<id>', views.article_Detail, name='article_Detail'),
    # path('cart/', views.cart, name='cart'),
    path('checkout1/', views.shipInfo, name='checkout1'),
    # path('store/', views.store, name='store'),
     # te gjitha url e cart
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:pk>/', views.remove_item, name='remove_item'),
    path('increase_item/<int:pk>/', views.increase_item, name='increase_item'),
    path('decrease_item/<int:pk>/', views.decrease_item, name='decrease_item'),
]

urlpatterns== static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)