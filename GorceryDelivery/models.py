from django.db import models
from StartupProject import settings
from django.contrib.auth.models import User

import datetime
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description= models.TextField()

    def __str__(self):
        return self.name + ": "+ self.description

    def get_name(self):
        return self.name

    def get_description(self):
        return  self.description

    def set_name(self, new_name):
        self.name = new_name

    def set_descriprion(self, new_description):
        self.description = new_description




class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, default=None, blank=True)
    img = models.ImageField( null=True,blank=True, upload_to='item_images/')
    discounted_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, default=0)


    def __str__(self):
        return self.name + ": " + self.description

    def get_price(self):
        return self.price

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_availability(self):
        return self.availability

    def get_discounted_price(self):
        return self.discounted_price

    def get_img(self):
        return  self.img

    def set_description(self, new_desc):
        self.description = new_desc

    def set_price(self, new_price):
        self.price = new_price

    def set_name(self, new_name):
        self.name = new_name

    def set_availability(self, new_availability):
        self.availability = new_availability

    def set_discounted_price(self, new_price):
        self.discounted_price = new_price




class UserProfile(models.Model):
    user_type = models.CharField(max_length=200, choices=( ('customer','customer'), ('staff', 'staff') ))
    gender = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    user = models.ForeignKey(User,models.CASCADE)

    def __str__(self):
        firstname_lastname = self.user.first_name + " " + self.user.last_name
        return firstname_lastname

    def get_userType(self):
        return self.user_type

    def get_gender(self):
        return self.gender


class Customer(models.Model):
    gender = models.CharField(max_length=200, choices=(('male','male'),('female','female')))
    phone_no = models.CharField(max_length=15)
    preffered_delivery_addr = models.TextField()
    alt_addr_1 = models.TextField(null=True, blank=True)
    alt_addr_2 = models.TextField(null=True, blank=True)
    user_profile = models.ForeignKey(UserProfile, models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user_profile) + ':' + self.get_gender()

    def get_gender(self):
        return self.gender

    def get_phone_no(self):
        return self.phone_no

    def get_customer_name(self):
        return self.user_profile

    def get_customer_email(self):
        profile = self.user_profile
        customer_user = profile.user
        customer_email = customer_user.email

        return customer_email

    def get_delivery_addr(self):
        return self.preffered_delivery_addr

    def get_alt_addr1(self):
        return self.alt_addr_1

    def get_alt_addr2(self):
        return self.alt_addr_2

    def set_phone_no(self,new_phone_no):
        self.phone_no = new_phone_no

    def set_delivery_addr(self, new_addr):
        self.preffered_delivery_addr = new_addr

    def set_alt_addr1(self, new_addr):
        self.alt_addr_1 = new_addr

    def set_alt_addr2(self, new_addr):
        self.alt_addr_2 = new_addr


class Order (models.Model):
    order_date = models.DateField(auto_now=True)
    order_time = models.TimeField(auto_now = True)
    paid_for = models.BooleanField()
    delivery_addr = models.TextField()
    delivery_date = models.DateField()
    buyer_firstname= models.CharField(max_length=200)
    buyer_lastname = models.CharField(max_length=200)
    buyer_gender = models.CharField(max_length=200, choices=( ('male','male'), ('female','female')))
    buyer_phone_no = models.CharField(max_length=15)
    buyer_email = models.EmailField(null=True, blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, default=None)
    order_total = models.DecimalField(decimal_places=2, max_digits=10)
    service_charge = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return "order for " + self.buyer_firstname +" " + self.buyer_lastname + " on " + str(self.order_date)

    def get_order_date(self):
        return self.order_date

    def get_service_charge(self):
        return  self.service_charge

    def get_order_time(self):
        return self.order_time

    def get_paid_for(self):
        return self.paid_for

    def get_delivery_date(self):
        return self.delivery_date

    def get_buyer_firstname(self):
        return self.buyer_firstname

    def get_buyer_lastname(self):
        return self.buyer_lastname

    def get_buyer_gender(self):
        return  self.buyer_gender

    def get_buyer_phone_no(self):
        return self.buyer_phone_no

    def get_buyer_email(self):
        return self.buyer_email

    def get_customer(self):
        return self.customer

    def get_order_total(self):
        return self.order_total

    def get_items_total(self):
        items_total = self.order_total - self.service_charge
        return  items_total

    def get_delivery_addr(self):
        return  self.delivery_addr

    def set_paid_for_True(self):
        self.paid_for = True

    def set_paid_for_False(self):
        self.paid_for = False



class SalesMeasure(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    item = models.ForeignKey(Item,models.CASCADE)

    def __str__(self):
        return self.name + " for " + str(self.item)

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_item(self):
        return self.item

    def set_description(self, new_description):
        self.description = new_description

    def set_price(self, new_price):
        self.price = new_price




class Presentation(models.Model):
    name = models.TextField()
    item = models.ForeignKey(Item, models.CASCADE)
    description = models.TextField()

    def __str(self):
        return self.name + " for " + self.name

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def set_description(self, new_description):
        self.description = new_description

class OrderItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    measure = models.ForeignKey(SalesMeasure, on_delete=models.SET_NULL, null=True, default=None)
    presentation = models.ForeignKey(Presentation, on_delete=models.SET_NULL, null=True, default=None )
    quantity = models.IntegerField(default=1)
    order_item_desc = models.TextField(null=True)
    order_item_price = models.DecimalField(decimal_places=2, max_digits=10 )
    price_by_qty = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.order) + ":  " + str(self.item)

    def get_item(self):
        return self.item

    def get_order(self):
        return self.order

    def get_price_by_qty(self):
        return self.price_by_qty

    def get_quantity(self):
        return self.quantity

    def get_order_item_price(self):
        return self.order_item_price

    def get_order_item_desc(self):
        return self.order_item_desc

    def get_presentation(self):
        return self.presentation

    def get_measure(self):
        return  self.measure

    def set_quantity(self, item_qty):
        self.quantity = item_qty

    def set_order_item_price(self, new_price):
        self.order_item_price = new_price



class Payment(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    description = models.TextField()
    transaction_reference = models.CharField(max_length=200)
    order = models.ForeignKey(Order,models.SET_NULL,null=True)
    status = models.CharField(max_length=200,null=True)

    def __str__(self):
        return  str(self.order) + " :" + str(self.timestamp)

    def get_timestamp(self):
        return self.timestamp

    def get_description(self):
        return self.description

    def get_trans_ref(self):
        return self.transaction_reference

    def get_order(self):
        return self.order

    def get_status(self):
        return self.status

    def get_payment_amount(self):
        the_order = self.order
        return the_order.get_order_total()

    def set_status(self, the_status):
        self.status = the_status

    def set_order_paidFor_true(self):
        self.order.set_paid_for_True()
        self.order.save()

    def set_description(self, desc_msg):
        self.description = desc_msg


class Shop(models.Model):
    shop_name = models.CharField(max_length=200, default='MarketWomanPH')
    phone_number = models.CharField(max_length=16, )
    phone_number_2 =  models.CharField(max_length=16,  null=True, default=None)
    address= models.TextField(default='Coca-cola junction, Trans-Amadi way')
    email = models.EmailField(default='hero4barca@gmail.com')
    site_domain = models.CharField(max_length=200, default='www.marketwoman.com.ng')
    service_charge = models.DecimalField(decimal_places=2, max_digits=15)
    is_active = models.BooleanField(default=False)


    def get_name(self):
        return self.shop_name

    def get_phoneNo(self):
        return  self.phone_number

    def get_alt_phoneNO(self):
        return self.phone_number_2

    def get_address(self):
        return self.address

    def get_email(self):
        return self.email

    def get_domain(self):
        return  self.site_domain

    def get_service_charge(self):
        return  self.service_charge


