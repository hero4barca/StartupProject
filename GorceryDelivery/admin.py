from django.contrib import admin

from django.contrib.admin import AdminSite
from django.http import HttpResponse, HttpResponseRedirect

from .models import Category,Item,SalesMeasure,Presentation,OrderItems,Order,Customer,Payment,Shop
from django.shortcuts import render,redirect
from django.contrib.admin import *

from GorceryDelivery.forms import OrderDisplayForm
from GorceryDelivery.modules.PDFGenerator import *
from GorceryDelivery.modules.AggregateOrderPDF import *
from datetime import datetime

class MyAdminSite(AdminSite):

    def __init__(self, *args, **kwargs):
        """
        allows complete inheritance from the default admin: default registration of USER and GROUP in admin
        :param args:
        :param kwargs:
        """
        super(MyAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)  # PART 2



    def get_urls(self):
        from django.urls import path,re_path
        urls = super().get_urls()
        urls += [

            path('customer_orders/', self.admin_view(self.get_daily_orders)),
            path('customer_orders/<str:delivery_date>/', self.admin_view(self.display_daily_orders)),
            re_path(r'^download_single_order/(\d+)/$', self.admin_view(self.download_single_order)),
            re_path(r'^customer_orders/details/(\d+)/$', self.admin_view(self.display_order_details)),
            path('customer_orders/items_by_day/<str:delivery_date>/', self.admin_view(self.aggregate_daily_orders))
            #path('customer_orders/print_all/<str:delivery_date>/', self.admin_view(self.print_orders_by_day))
        ]
        return urls


    def get_daily_orders(self, request):
        """
        View function: allows displays of all order given a specific delivery date
        :param request: Http request
        :return: Http redirect to display page; if method is not 'POST', renders delivery date form 
        """

        if request.method == 'POST':
            form = OrderDisplayForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                next_url = '/admin/customer_orders/' + cd.get('date') + '/'
                #assert False
                return HttpResponseRedirect(next_url)# redirect to url of 'display daily orders'

        else:
            form = OrderDisplayForm()

        return  render(request, 'admin/get_orders.html', {'form': form})


    def display_daily_orders(self, request, delivery_date):
        """
        View function: actually dispays the orders
        :param request: Http request
        :param delivery_date: delivery date to query
        :return: renders a tabled list of all the orders
        """

        date_error = False
        # convert the date first
        try:#since date input is exposed using get: anticipating incorrect input
            objDate = datetime.strptime(delivery_date, '%d-%m-%Y')
            delivery_date = objDate.strftime('%Y-%m-%d')
        except:
            delivery_date = None
            date_error = True

        date_orders = Order.objects.filter(delivery_date=delivery_date)

        return render(request, 'admin/show_orders.html', {'orders': date_orders,
                                                          'date': delivery_date,
                                                          'date_error': date_error})


    def download_single_order(self, request, order_Id):
        """
        View function: downloads the user order form the 'display daily orders' list as pdf
        :param request: Http request
        :param order_Id: pk of the order in db
        :return: pdf file as Http response
        """

        bought_items = None
        order_details = None

        order_Id = int(order_Id)

        try:
            order_details = Order.objects.get(id=order_Id)
        except:
            order_details = None

        bought_items = OrderItems.objects.filter(order=order_details)

        if not bought_items == None:
            the_report = PDFGenerator(order_details, bought_items)
            return the_report.download_user_order()



    def display_order_details(self, request, order_id):
        """
        View function: displays the details of a selected custmer order
        :param request: Http request
        :param order_id: pk of the selected order
        :return: renders the details 
        """

        order_details = None
        bought_items = None
        order_id = int(order_id)

        try:
            order_details = Order.objects.get(id=order_id)
        except:
            order_details = None

        bought_items = OrderItems.objects.filter(order=order_details)


        return render(request,'admin/display_order_details.html', { 'order': order_details,
                                                                    'bought_items': bought_items})



    def aggregate_daily_orders(self, request, delivery_date):
        """
        View Function: downloads aggregated orders for a given date showi ng an item and how many times it was ordered.
        :param request: Http request
        :param delivery_date: delivery date
        :return: pdf file as http response
        """

        date_error = False
        try:
            objDate = datetime.strptime(delivery_date, '%Y-%m-%d')
            delivery_date = objDate.strftime('%Y-%m-%d')
        except:
            date_error = True

        order_items_list = []

        if not date_error:
            order_list = Order.objects.filter(delivery_date = delivery_date)
            for order in order_list:
                item_list = OrderItems.objects.filter(order= order)
                order_items_list.append(item_list)


            daily_order = AggregateOrderPDF(order_items_list, delivery_date)
            daily_order.compute_aggregate_list()
            return  daily_order.download_aggregate_order()

        #assert False





admin_site = MyAdminSite()



@admin.register(Item, site= admin_site)
class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'discounted_price', 'availability')
    list_filter = ('category', 'availability')
    search_fields = ('name',)
    list_per_page = 10



@admin.register(Category, site =admin_site)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_per_page = 10
    search_fields = ('name',)



@admin.register(Customer, site =admin_site)
class AdminCustomer(admin.ModelAdmin):
    list_display = ('user_profile','gender', 'phone_no', 'preffered_delivery_addr')
    list_per_page = 10



@admin.register(Order, site=admin_site)
class AdminOrder(admin.ModelAdmin):
    list_display =('buyer_firstname', 'buyer_lastname', 'buyer_gender','buyer_email', 'buyer_phone_no',
                   'order_date', 'paid_for','delivery_date','order_total','delivery_addr', 'customer' )
    list_per_page = 10
    list_filter = ('buyer_gender', 'paid_for', 'order_date', 'delivery_date')
    search_fields = ( 'buyer_firstname', 'buyer_lastname','buyer_phone_no','buyer_email')




@admin.register(SalesMeasure, site =admin_site)
class AdminSalesMeasure(admin.ModelAdmin):
    list_display = ('name','description', 'item', 'price')
    list_per_page = 10
    search_fields = ('item__name','name')
    list_filter = ('item',)



@admin.register(Presentation, site =admin_site)
class AdminPresentation(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('name', 'description', 'item')



@admin.register(Payment, site =admin_site)
class AdminPayment(admin.ModelAdmin):
    list_display = ('description', 'payment_type', 'timestamp', 'token_identifier', 'order')
    list_per_page = 10



@admin.register(OrderItems, site=admin_site)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ('order_item_desc', 'order_item_price', 'quantity', 'price_by_qty')
    list_per_page = 10
    list_filter = ('item', 'order')
    search_fields = ('item__name', 'order__buyer_firstname')


@admin.register(Shop, site=admin_site)
class Shop(admin.ModelAdmin):
    list_display = ('shop_name','site_domain', 'address', 'email', 'phone_number', 'phone_number_2', 'is_active')
