

from django import forms
from GorceryDelivery.models import *
from datetime import date
import re
import calendar

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'Firstname'}))
    lastname = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'Lastname'}))
    email = forms.CharField(max_length=100,
                            widget=forms.EmailInput
                            (attrs={'placeholder': 'Email Address'}))
    username = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'Username'}))
    phonenumber = forms.CharField(max_length=100,
                                  widget=forms.TextInput
                                  (attrs={'placeholder': 'Phone Number'}))

    address = forms.CharField(max_length=150,
                                  widget=forms.Textarea
                                  (attrs={'placeholder': 'Main address',
                                   'cols':'31'}))
    alt_address_1 = forms.CharField(max_length=150,required=False,
                              widget=forms.Textarea
                              (attrs={'placeholder': '(optional) alternative addr 1',
                                      'cols':'31'}))
    alt_address_2 = forms.CharField(max_length=150, required=False,
                                    widget=forms.Textarea
                                    (attrs={'placeholder': '(optional) alternative addr 2',
                                            'cols':'31'}))
    gender = forms.CharField(label='Gender',widget=forms.RadioSelect(attrs={'class': 'gender'},choices=[
                                                                ('male','male'),
                                                                 ('female','female')]))

    password = forms.CharField(widget=forms.PasswordInput
                                (attrs={'placeholder': 'Password'}))

    password_repeat = forms.CharField(widget=forms.PasswordInput
    (attrs={'placeholder': 'Repeat Password'}))


    def clean(self):
        """
        custom clean function to validate that both passwords match
        :return:
        """

        cd = super(RegistrationForm,self).clean()

        cd_password = cd.get('password')
        cd_password_repeat = cd.get('password_repeat')
        cd_email = cd.get('email')
        cd_phone_number = cd.get('phonenumber')
        cd_username = cd.get('username')


        if not cd_password == cd_password_repeat:
            self.add_error('password_repeat','repeat password must match password')

        if '@' not in cd_email or '.' not in cd_email:
            self.add_error('email', 'please enter valid email')

        if len(cd_phone_number) < 6:
            self.add_error('phonenumber','phone number appears too short')

        duplicate_username= User.objects.filter(username=cd_username)

        if duplicate_username:
            self.add_error('username', 'username already taken, change username')



class OrderForm(forms.Form):

    firstname = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'Firstname'}))
    lastname = forms.CharField(max_length=100,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Lastname'}))


    email = forms.CharField(max_length=100,
                            widget=forms.EmailInput
                            (attrs={'placeholder': 'Email Address'}))

    phonenumber = forms.CharField(max_length=100,
                                  widget=forms.TextInput
                                  (attrs={'placeholder': 'Phone Number'}))
    delivery_address = forms.CharField(max_length=150,
                              widget=forms.Textarea
                              (attrs={'placeholder': 'Main address- please include landmarks',
                                      'cols': '31'}))
    gender = forms.CharField(label='Gender', widget=forms.Select(choices=[ ('',''),
                                                                            ('male', 'male'),
                                                                             ('female', 'female')]))
    address_type = forms.CharField(label='Address type', required=False, widget=forms.Select( choices=[('',''),
                                                                                                       ('home', 'home'),
                                                                                                        ('office', 'office')]))
    delivery_date = forms.CharField(widget=DateInput())



    def clean(self):
        cd = super(OrderForm, self).clean()

        cd_email = cd.get('email')
        cd_phone_no = cd.get('phonenumber')
        cd_delivery_addr = cd.get('delivery_address')
        cd_delivery_date = cd.get('delivery_date')

        dateArry = re.split('-',cd_delivery_date)

        date_error = False
        try:
            delv_date = datetime.date(int(dateArry[2]),int(dateArry[1]),int(dateArry[0]))
        except:
            self.add_error('delivery_date','invaid date, use "dd-mm-yyyy format"')
            date_error = True

        if '@' not in cd_email or '.' not in cd_email:
            self.add_error('email', 'please enter valid email')

        if len(cd_phone_no) < 6:
            self.add_error('phonenumber','phone number appears too short')

        if len(cd_delivery_addr) < 10:
            self.add_error('delivery_address','delivery address appears too short' )

        #the date input is valid but not " Tomorrow" at least
        if not date_error:
            if not delv_date> date.today():
                self.add_error('delivery_date','delivery date must be at least a day after order is placed')

            weekday = calendar.day_name[delv_date.weekday()]
            if weekday == 'Sunday':
                self.add_error('delivery_date', 'We do not make deliveries on Sundays')




class PaymentForm(forms.Form):

    name_on_card = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'John Smith', 'class':'form-control'}))

    card_number = forms.CharField( max_length=19,
                                   widget=forms.TextInput
                                (attrs={ 'class':'form-control',
                                         'placeholder': 'XXXX XXXX XXXX XXXX'}))

    cvv = forms.CharField( max_length=4,
                          widget=forms.TextInput(
                              attrs={'class':'form-control',
                                     'placeholder':'CVV'}
                          ))

    expiration_date = forms.CharField(max_length=5,
                                      widget=forms.TextInput(
                                          attrs={'class':'form-control',
                                                 'placeholder':'dd/yy'}
                                      ))

    #TODO: propper cleaning and definition of validation for form when implementing payment



class OrderDisplayForm(forms.Form):

    date = forms.CharField(widget=DateInput())


    def clean(self):
        cd = super(OrderDisplayForm, self).clean()

        cd_date = cd.get('date')

        dateArry = re.split('-', cd_date)

        try:
            delv_date = datetime.date(int(dateArry[2]), int(dateArry[1]), int(dateArry[0]))
        except:
            self.add_error('date', 'invaid date, use "dd-mm-yyyy format"')



class PasswordResetDetailsForm(forms.Form):

    email =forms.CharField(max_length=100,
                            widget=forms.EmailInput
                            (attrs={'placeholder': 'Email Address'}))

    username = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'placeholder': 'Username'}))



    def clean(self):

        cd = super(PasswordResetDetailsForm, self).clean()

        cd_email= cd.get('email')
        cd_username = cd.get('username')

        if '@' not in cd_email or '.' not in cd_email:
            self.add_error('email', 'please enter valid email')

        try:

            the_user = User.objects.get(email= cd_email, username= cd_username, )
        except:
            raise  forms.ValidationError('A user account matching the details provided was not found')

        return cd



class UpdatePasswordForm(forms.Form):

    new_password = forms.CharField(widget=forms.PasswordInput
                                (attrs={'placeholder': 'password'}))

    repeat_password =  forms.CharField(widget=forms.PasswordInput
                                (attrs={'placeholder': 'confirm password'}))



    def clean(self):
        cd = super(UpdatePasswordForm, self).clean()

        new_password = cd.get('new_password')
        repeat_password = cd.get('repeat_password')

        if not new_password == repeat_password:
            raise  forms.ValidationError('password inputs do not match')

        return cd






