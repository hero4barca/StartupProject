"""StartupProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from django.urls import path,re_path
from django.contrib.auth import login,logout
from GorceryDelivery.views import *
from django.contrib.auth import views as auth_views

# for serving the item_images in debug mode through 'django.contrib.staticfiles.views.serve()' view
from django.conf import settings
from django.conf.urls.static import static

from GorceryDelivery.admin import admin_site, AdminSite

admin.autodiscover()

AdminSite.site_header= "Market Woman Administration"
AdminSite.site_title = "Market Woman Admin"
AdminSite.index_title = "Market Woman"

admin_site.site_header = "Market Woman Administration"
admin_site.site_title = "Market Woman Admin"
admin_site.index_title = "Market Woman"

urlpatterns = [

    path('admin/', admin_site.urls),#admin site

    re_path(r'^$', index), #url config for site root
    path('index/', index),
    path('about/', about),
    path('contact/',contact),
    path('policy/', policy),

    path('success/<str:action>/', success),

    #categories
    path('categories/', list_all_categories),#page list's all item categories
    re_path(r'^categories/(\d+)/$', show_category_items),# show items by categories
    path('generic_items/', show_generic_items), # generic items

    path('search_items/', ajax_search, name="search_items"),

    re_path(r'^item_details/(\d+)/$', item_details ), # displays detailed item page

    path('add_order_item/', add_order_item),# add an item to shopping cart
    path('remove_order_item/<str:name>/<str:description>/', remove_order_item), # removes item from shopping cart

    path('sign_up/', register_customer), # reigister's customer

    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),#login
    path('accounts/profile/', user_account ),# redirect to create user sessions after successful login
    path('logout/', auth_views.LogoutView.as_view(next_page='/index/')),# logout
    path('accounts/customer/', customer_account),# customer account page to display customer transactions

    #for password reset calls
    re_path('^', include('django.contrib.auth.urls')),

    path('order/checkout/', checkout),# for checkout of items: allows editing (qty) and removing items
    path('qty_minus/<str:name>/<str:description>/', reduce_item_qty),
    path('qty_plus/<str:name>/<str:description>/', increase_item_qty),

    path('order/confirm_details/', confirm_order_details),# displays all order details for cnfirmation by user
    path('order/payment/', make_payment),# to payment page

    #******* Needed?
    path('order/save_order/', create_new_order),

    path('order/show_receipt/', show_order_receipt),
    path('order/download_receipt/', single_orderPDF ),

    #per Cash Envoy
    path('order/payment2/',make_payment2),
    path('order/payment_complete/', payment_complete),

    #****Vouge Pay integrating URLS
    #path('order/payment/', make_payment1),# to payment page
    #path('order/show_receipt/<int:order_id>', show_order_receipt1),
    #path('order/failure/<int:order_id>', vouge_failure),


    path('check/',check_sess),


]

# for displaying the item_images in debug mode
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)