from django.shortcuts import render,redirect
from GorceryDelivery.models import *
from GorceryDelivery.modules.ItemsInOrder import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from GorceryDelivery.forms import *

import random
from GorceryDelivery.modules.PDFGenerator import *

from decimal import Decimal
from datetime import datetime

#for ajax request
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from io import BytesIO


def read_all_categories():
    """
    function to read all categories currently in the db
    :return: a queryset of all categories in the db
    """
    try:
        all_categories = Category.objects.all()
    except:
        all_categories = None

    return all_categories



def assign_column_number(the_queryset):
    """
    function:creates a list of dict with data relevant to template display
    :param the_queryset: all item of a chosen category
    :return: display list - a list of dict containing the item, colum number (i.e. 1,2,3 or 4) and last ietm flag
    """
    column_num = 1
    item_n_col = {}
    display_list = []
    count = 0
    for item in the_queryset:
        count = count + 1
        item_n_col['col_num'] = column_num
        item_n_col['item'] = item
        item_n_col['last'] = False

        if count == the_queryset.count(): #if item is the last in query set
            item_n_col['last'] = True

        display_list.append(item_n_col.copy())

        if column_num == 4:
            column_num = 1
        else:
            column_num = column_num +1

    return display_list



def clear_order_sessions(request):
    """
    function: clears all order related session variables after the
    processing of an order has been successfully completed.
    :param request:
    :return:
    """

    if 'items_in_order' in request.session:
        del request.session['items_in_order']

    if 'current_total' in request.session:
        del  request.session['current_total']

    #if 'service_charge' in request.session:
        #del request.session['service_charge']

    if 'ord_firstname' in request.session:
        del request.session['ord_firstname']

    if 'ord_lastname' in request.session:
        del request.session['ord_lastname']

    if 'ord_email' in request.session:
        del request.session['ord_email']

    if 'ord_gender' in request.session:
        del request.session['ord_gender']

    if 'ord_phone_no' in request.session:
        del request.session['ord_phone_no']

    if 'ord_delivery_date' in request.session:
        del request.session['ord_delivery_date']

    if 'ord_delivery_address' in request.session:
        del request.session['ord_delivery_address']

    if 'total_plus_serviceCharge' in request.session:
        del request.session['total_plus_serviceCharge']

    return



def display_items():
    """
    randomly selects four items to be displayed on the index page -'pouplar items'
    :return: sample_list - a list of randomly selected items
    """
    sample_list = []

    items_list = Item.objects.all()

    for i in range(0,4):#select four random items for display
        item = None
        while (item == None):#loop runs until a valid item is selected
            random_id = random.randint(1, items_list.last().pk)# range: 1, pk of last item in item_list
            item= items_list.filter(id=random_id).first()#'first' to retrieve the item from the queryset of one item

            if item in sample_list:#  avoid selection of duplicates
                item = None

            if not item == None: #avoid selection of unavailable items
                if item.get_availability() == False:
                    item = None

        sample_list.append(item)

    return sample_list


#view functions below

def index(request):
    """
    displays index page
    :param request: http request
    :param categories: all categories in the db for display
    :return: http request
    """

    all_categories = read_all_categories()
    sample_items = display_items()


    return render(request, 'index.html', {'categories':all_categories,
                                          'sample_items': sample_items})



def about(request):
    """
        displays about page
        :param request: http request
        :param categories: all categories in the db for display
        :return: http request
        """
    all_categories = read_all_categories()


    return render(request, 'about.html', {'categories': all_categories})



def contact(request):
    """
            displays contact_us page
            :param request: http request
            :param categories: all categories in the db for display
            :return: http request
            """

    all_categories = read_all_categories()
    errors = []
    email_success = False

    if request.method == 'POST':

        if not request.POST.get('Name',''):
            errors.append('Please enter your name!')
        else:
            name = request.POST.get('Name','')

        if not request.POST.get('Email',''):
            errors.append('Please enter your email address!')
        else:
            if '@' not in request.POST.get('Email','') or '.' not in request.POST.get('Email',''):
                errors.append('Please enter a valid email address: "you@example.com" ')
            else:
                sender_email = request.POST.get('Email','')

        if not request.POST.get('Telephone',''):
            errors.append('Please enter your phone number!')
        else:
            if len(request.POST.get('Telephone', '')) < 8:
                errors.append('Please enter a valid phone number !')
            else:
                telephone = request.POST.get('Telephone','')

        if not request.POST.get('Subject',''):
            errors.append('A subject is required!')
        else:
            subject = request.POST.get('Subject','')

        if not request.POST.get('Message',''):
            errors.append('Mesage required!!')
        else:
            message = request.POST.get('Message','')

        #assert False
        subject = ' Contact Mail - ' + subject

        message += '\n\n'
        message += '*****SENDER DETAILS*******'
        message +=  '\nSender Email: ' + sender_email + '\nSender Phone No: ' + telephone

        if len(errors) < 1:
            #pass #send email here
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['marketwomanPH@gmail.com'],
                    fail_silently=False,
                )
                email_success = True
            except:
                errors.append("There was an issue sending this mail, please try again...")

            if email_success == True:
                return HttpResponseRedirect('/success/email/')

    return render(request, 'contact.html', {'categories': all_categories,
                                            'errors':errors})



def password_reset(request):
    """
    View function: main function for pasword reset
    :param request: HTTP request
    :return: HTTP redirect for successfully sending password reset email; renders reset page if method is not 'POST'
    """

    status = True
    if request.method == 'POST':
        form = PasswordResetDetailsForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data


            the_user = User.objects.get(email=cd.get('email'), username =cd.get('username') )
            the_profile = UserProfile.objects.get(user=the_user)
            the_customer = Customer.objects.get(user_profile__user=the_user)

            try:
                shop_details = Shop.objects.get(email=settings.EMAIL_HOST_USER)
                domain = shop_details.get_domain()
            except:
                status = False

            reset_link = domain + '/change_password/' + str(the_user.id) + '/' + str(the_profile.id) + '/' + str(
                the_customer.id) + '/'

            subject = 'Market woman: password reset'
            message = 'Dear ' + cd.get('firstname')+ ',\n\n' \
                      'You can use the link below to reset your password. Please ignore this message if you did not initiate this. \n ' \
                      '     ' + reset_link + ' \n\n' \
                                             'marketwomanPH '
            #assert False

            if status:
                try:
                    send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [cd.get('email')]
                    )
                except:
                    status = False
            #assert False
            if status:
                return HttpResponseRedirect('/success/password_reset/')

    else:

        form = PasswordResetDetailsForm()

    return render(request,'reset_password.html',{'form': form,
                                                 'status': status})



def change_password(request, user_id, profile_id, customer_id):
    """
    View function: Handles the link generated and sent to the email of a customer for password recovery
    verifies the link and redirects to update password page if valid
    :param request: HTTP request
    :param user_id: user ID
    :param profile_id: user_profile ID
    :param customer_id: customer_id
    :return: HTTP response or redirect
    """

    verify = True

    try:
        the_user = User.objects.get(id= user_id)
        the_profile = UserProfile.objects.get(id= profile_id, user = the_user)
        the_customer = Customer.objects.get(id= customer_id, user_profile= the_profile)
    except:
        verify = False

    if verify == True:
        request.session['update_password_user'] = user_id
        return  HttpResponseRedirect('/update_password/')
    else:
        return HttpResponse('The request is invalid, please use the link that was sent to you via email')





def update_password(request):
    """
    View function: allows user to actually update the password
    :param request: HTTP request
    :return: HTTP redirect for successful update or renders 'password update form' is request method isn't 'POST'
    """

    if not 'update_password_user' in request.session:
        return HttpResponse('This request in invalid, please use the link that was sent to you via email')

    update = True

    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_password = cd.get('new_password')

            try:
                the_user = User.objects.get(id = int(request.session['update_password_user']))

                the_user.set_password(new_password)
                the_user.save()
            except:
                update = False
            #assert False
            if update == True:
                del request.session['update_password_user']
                return HttpResponseRedirect('/success/password_update/')

    else:
        form = UpdatePasswordForm()


    #assert False
    return render(request, 'update_password.html', {'form': form,
                                                    'update': update})

def policy(request):
    """
            displays policy page
            :param request: http request
            :param categories: all categories in the db for display
            :return: http request
            """
    all_categories = read_all_categories()

    return render(request, 'policy.html', {'categories': all_categories})




def list_all_categories(request):
    """
    :param request: http request
    :return: http request
    """
    all_categories = read_all_categories()
    return render(request, 'list_categories.html', {'categories': all_categories})




def ajax_search(request):
    """
    Ajax View Function: handles search for items form db
    :param request: Http request
    :return: a list of matching items
    """

    url_parameter = request.GET.get("q")

    if url_parameter:
        items = Item.objects.filter(name__icontains=url_parameter)
    else:
        items = Item.objects.all()

    #handling ajax request

    if request.is_ajax():

        if not url_parameter =='':
            search_result = True
        else:
            search_result = False


        html = render_to_string(
                template_name= 'search-results-partial.html',
                context={'items': items,
                         'display': search_result}
            )

        data_dict = {'html_from_view': html}
        return JsonResponse(data=data_dict, safe=False)

    return redirect(request.META['HTTP_REFERER'])




def show_category_items(request, id_category):
    """
    :param request: http request
    :param id_category: category identifier(pk)
    :return: http request
    """
    all_categories = read_all_categories()
    items_in_category = Item.objects.filter(category_id=id_category)
    the_category = all_categories.get(pk=int(id_category))
    items_n_col = assign_column_number(items_in_category)

    return render(request,'category_items.html',{'grid_items': items_n_col,
                                                 'categories': all_categories,
                                                 'current_category': the_category,
                                                 })





def show_generic_items(request):
    """
    for display of generic items that are not categorized
    :param request: http request
    :return: http request
    """

    all_categories = read_all_categories()
    items_in_category = Item.objects.filter(category = None)
    items_n_col = assign_column_number(items_in_category)

    return render(request,'generic_items.html', {'grid_items': items_n_col,
                                                 'categories': all_categories,
                                                 })





def item_details(request, id_item):
    """
    detailed display of food items
    :param request:
    :param id_item: pk of item
    :return: http request
    """
    all_categories = read_all_categories()
    sales_measures = SalesMeasure.objects.filter(item_id=id_item)
    presentation = Presentation.objects.filter(item_id=id_item)

    try:
        the_item=Item.objects.get(id= id_item)
    except:
        the_item = None

    return render (request,'single_item.html', {'item': the_item,
                                                'categories': all_categories,
                                                'measure': sales_measures,
                                                'presentation': presentation})





def add_order_item(request):
    """
    called on request
    :param request:
    :return:
    """
    order_item_list=[]
    current_total = 0

    if request.method == 'POST':
        new_order_item = ItemsInOrder()
        new_item_details = new_order_item.order_item_details(request)


        if new_item_details:
            if 'items_in_order' not in request.session or not request.session['items_in_order']:
                order_item_list.append(new_item_details)
                request.session['items_in_order'] = order_item_list.copy()
                request.session.set_expiry(43200)
            else:
                order_item_list = request.session['items_in_order']
                order_item_list.append(new_item_details.copy())
                request.session['items_in_order'] = order_item_list.copy()

        for item in request.session['items_in_order']:
            item_qty = int(item['qty'])
            current_total = Decimal(current_total) + (Decimal(item['price']) *item_qty)
        request.session['current_total'] = str(current_total)

    #return HttpResponse(request.session['items_in_order'])
    return redirect(request.META['HTTP_REFERER'])





def remove_order_item(request, name):
    """
    :param request:
    :param name:
    :return:
    """
    order_items_list = []

    if 'items_in_order' in request.session:

        order_items_list = request.session['items_in_order']
        for item in order_items_list:
            if item['name'] == name:
                order_items_list.remove(item)

                if request.session['current_total']:
                    new_total= Decimal(request.session['current_total']) - Decimal( item['price'])
                    request.session['current_total']= str(new_total)

        if len(order_items_list) == 0:
            clear_order_sessions(request)
        else:
            request.session['items_in_order'] = order_items_list.copy()

    return redirect(request.META['HTTP_REFERER'])




def register_customer(request):
    """
    registers a new user as customer
    :param request:
    :return: to success page
    """

    all_categories = read_all_categories()
    success = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd= form.cleaned_data

            new_user = User.objects.create_user(username=cd['username'], email=cd['email'],
                                                    password=cd['password'], first_name=cd['firstname'],
                                                    last_name=cd['lastname']
                                                    )
            new_user.save()

            new_userprofile = UserProfile(user=new_user, user_type='customer',gender=cd['gender'])
            new_userprofile.save()

            new_customer = Customer(user_profile=new_userprofile, phone_no=cd['phonenumber'], gender=cd['gender'],
                                    preffered_delivery_addr=cd['address'], alt_addr_1=cd['alt_address_1'],
                                    alt_addr_2=cd['alt_address_2'])
            new_customer.save()

            success = True

            subject = 'Welcome mail - Market Woman'
            message = 'Dear' + cd['firstname'] + ',\n\n'
            message += 'We are pleased to confirm your registration as a customer of market woman.' \
                       'Your account details are as follows: \n' \
                       '    Name: ' + cd['firstname'] + ' ' + cd['lastname'] + '\n' \
                       '    Username: ' + cd['username'] +'\n\n' \
                       'We look forward to helping you satisfy your grocery needs.\n' \
                                                      'Market Woman PH'

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [cd['email']]
                )

            except:
                pass
            return  HttpResponseRedirect('/success/registration/')#returns to success page

    else:
        form = RegistrationForm()

    return render(request, 'register.html',{'categories': all_categories,
                                            'form':form,
                                           })




def user_account(request):
    """
    redirects here after user login is successful
    :param request:
    :return: a redirect to index page
    """
    current_user_profile = UserProfile.objects.get(user=request.user)

    if 'usertype' not in request.session:
        request.session['usertype'] = current_user_profile.get_userType()
        request.session['username'] = request.user.get_username()


    return HttpResponseRedirect('/index/')




def success(request, action):
    """
    success page
    :param request:
    :param event:
    :return:
    """
    all_categories = read_all_categories()
    return render(request, 'success.html', {'action': action,
                                            'categories': all_categories})

def aggregate_item_qty(request):
    """
    view renders checkout page; aggregates item qty by increasing qunatity and deleting duplicates
    :param request: http request
    :return: http request
    """

    checkout_items = []

    if 'items_in_order' in request.session:
        checkout_items = request.session['items_in_order']
        no_of_items = len(checkout_items)
        #resolve multiple item by removing increasing the qty and removing deplicate from list
        for index1, item1 in enumerate(checkout_items):
            for index2, item2 in enumerate(checkout_items):
                # compare items, not same index AND same item id
                if not index1 == index2:
                    if item1['id'] == item2['id']:
                        qty = int(item1['qty'])  # increase qty of 1st item
                        qty = qty + 1
                        item1['qty'] = qty
                        del checkout_items[index2]

        request.session['items_in_order'] = checkout_items.copy()
    return




def checkout(request):
    """
    first-calls aggregate_item_qty to clean up qty of order items
    :param request: http request
    :return: http request
    """

    # ensure that shop_is_active session is true before proceeding

    shop = Shop.objects.filter(shop_name =request.session['shop_name']).first()
    if not shop.is_active:
        return HttpResponse(' Checkout is temporarily unavailable. Please contact MarketWomanPh for details.')


    initial_data = {}
    aggregate_item_qty(request) # to clean up qty

    if 'usertype' in  request.session:
        current_user = request.user
        customer_data = Customer.objects.get(user_profile__user=current_user)
        initial_data['firstname'] = request.user.first_name
        initial_data['lastname'] = request.user.last_name
        initial_data['email'] = request.user.email
        initial_data['phonenumber'] = customer_data.get_phone_no()
        initial_data['delivery_address'] = customer_data.get_delivery_addr()
        initial_data['gender'] = customer_data.get_gender()


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            #create order_details in session

            request.session['ord_firstname'] = request.POST['firstname']
            request.session['ord_lastname'] = request.POST['lastname']
            request.session['ord_gender'] = request.POST['gender']
            request.session['ord_phone_no'] = request.POST['phonenumber']
            request.session['ord_email'] = request.POST['email']
            request.session['ord_delivery_date'] = request.POST['delivery_date']
            request.session['ord_delivery_address'] = request.POST['delivery_address']

            if not request.POST['address_type'] == '':
                request.session['ord_delivery_address'] = request.session['ord_delivery_address'] + ' [' + request.POST['address_type'] + ']'
            #move to payment
            return redirect('/order/confirm_details/')
    else:

        if 'usertype' in request.session:#  user is signed in
            form = OrderForm(initial=initial_data)
        else: # user not signed in
            form = OrderForm()

    return render (request, 'checkout.html',{'form': form})




def reduce_item_qty(request, item_name):
    """
    reduces item qty on checkout; also adjusts current total accordigly
    :param request:
    :param item_name:
    :return:
    """
    order_items_list = []
    if 'items_in_order' in request.session:
        order_items_list = request.session['items_in_order']
        for index, item in enumerate(order_items_list):
            if item['name'] == item_name:
                current_qty = int(item['qty'])
                if current_qty == 1:# if item qty =1; call remove it
                    return remove_order_item(request,item_name)
                if current_qty > 1:# subtract qty and update sessions var
                    current_qty = current_qty -1
                    order_items_list[index]['qty'] = current_qty

                    #modify current total session variable
                    new_total = Decimal(request.session['current_total']) - Decimal(item['price'])
                    request.session['current_total'] = str(new_total)

                    request.session['items_in_order'] = order_items_list.copy()

    return redirect(request.META['HTTP_REFERER'])




def add_item_qty(request, item_name):
    """
    increases item qty on checkout; also adjusts current total accordingly
    :param request:
    :param item_name:
    :return:
    """
    order_items_list = []
    if 'items_in_order' in request.session:
        order_items_list = request.session['items_in_order']

        for index, item in enumerate(order_items_list):
            if item['name'] == item_name:
                current_qty = int(item['qty'])
                #if current_qty > 1:
                current_qty = current_qty + 1
                order_items_list[index]['qty'] = current_qty

                # modify current total session variable
                new_total = Decimal(request.session['current_total']) + Decimal(item['price'])
                request.session['current_total'] = str(new_total)

                request.session['items_in_order'] = order_items_list

    return redirect(request.META['HTTP_REFERER'])




def confirm_order_details(request):
    """
    shows the final details of order before the payment page
    :param request: HTTP requests
    :return:
    """



    if 'current_total' in request.session:
        if not 'service_charge' in request.session:#  add service charge to cost
            try:
                service_charge = Shop.objects.get(shop_name='market_woman').get_service_charge()
            except:
                service_charge = 1000
            request.session['service_charge'] = str(service_charge)

    if 'current_total' in request.session and 'service_charge' in request.session:
        new_total = Decimal(request.session['current_total']) + Decimal(request.session['service_charge'])
        request.session['total_plus_serviceCharge'] = str(new_total)
    #assert False
    return  render( request, 'order_details.html')




def create_new_order(request):
    """
    Creates new order object and save to database,
    ****NOTE: does not set paid_for attribute of the new order object to true.
    :param request: Http request
    :return: new order object if successful; false if not successful
    """
    new_order = None

    #convert the date first
    delivery_date = request.session['ord_delivery_date']
    objDate = datetime.strptime(delivery_date, '%d-%m-%Y')
    delivery_date = objDate.strftime( '%Y-%m-%d')

    if 'items_in_order' in request.session:

        order_items_list = request.session['items_in_order']
        current_customer = None
        success = True

        #retive customer object if the current user signed in as a customer
        if 'usertype' in request.session:

            try:
                current_customer = Customer.objects.get(user_profile__user= request.user)
            except:
                current_customer = None


        #create order object and save to db
        try:

            new_order = Order(buyer_firstname=request.session['ord_firstname'],
                                             buyer_lastname= request.session['ord_lastname'],
                                             buyer_email= request.session['ord_email'],
                                             buyer_gender= request.session['ord_gender'],
                                             buyer_phone_no= request.session['ord_phone_no'],
                                             delivery_date = delivery_date,
                                             delivery_addr= request.session['ord_delivery_address'],
                                             paid_for= False,
                                             order_total= Decimal(request.session['total_plus_serviceCharge']),
                                             service_charge= Decimal(request.session['service_charge']),
                                             customer= current_customer)
        #assert False
            new_order.save()
        except:
            success = False

        #create orderItmes and save to db
        if success == True:  # do not create orderItems if order wasn't successfully created
            for item in order_items_list:

                #*** assign presentation
                if 'presentation' in item:
                    try:
                        item_presentation = Presentation.objects.get(id= int(item['presentation']))
                    except:
                        item_presentation = None
                else:
                    item_presentation = None

                #****assign Market Measure
                if 'market_measure' in item:
                    try:
                        item_measure = SalesMeasure.objects.get(id = int(item['market_measure']))
                    except:
                        item_measure = None
                else:
                    item_measure = None

                try:
                    new_order_item = OrderItems(order= new_order,
                                                        item_id= int(item['id']),
                                                        quantity= int(item['qty']),
                                                        order_item_price =  Decimal(item['price']),
                                                        price_by_qty=  Decimal(item['price'])*int(item['qty']),
                                                        order_item_desc= item['description'],
                                                        measure= item_measure,
                                                        presentation= item_presentation
                                                            )
                    new_order_item.save()

                except:
                    new_order.delete()#delete the order object(not order object with corresponding order items); cascade delete FK
                    success = False
                    break  # do not create any more orderitems


        if not success: #if creating the new order/orderItems was not 'hitch-free'
            return False
        else:
            return new_order





def make_payment(request):
    """
     View function: allows payment
    :param request: Http request
    :return:
    """
    payment_successful = False # payment placeholder

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():

            current_order = create_new_order(request)

            if not current_order == False:#ensures that order has been successfully created
                # TODO sort out payment first before order/order items (i.e.) payment in db
                # code to integrate with merchant here
                payment_successful = True #PLACEHOLDER FLAG


                #AFTER successful payment
                #****if payment is successful
                current_order.set_paid_for_True()
                current_order.save()

                clear_order_sessions(request)


                #get the ID of current_order, put it in a session and retrieve at 'show_order_reciept
                request.session['order_ID'] = str(current_order.id)

            #call show order reciept
            return redirect ('/order/show_receipt/')


    else:
        form = PaymentForm()

    return render(request, 'payment.html',{'form': form})





def show_order_receipt(request):
    """
    View function: shows the reciept or confirmation of payment after successful payment processing
    allows link for downloading of order reciept
    sends order confirmation email to customer
    :param request:
    :param the_order:
    :return:
    """
    bought_items=None
    the_order = None
    
    if 'order_ID' in request.session:
        try:
            the_order = Order.objects.get(id= int(request.session['order_ID']))
        except:
            the_order = None

    send_order_confirmation_email(request, the_order)
    bought_items = OrderItems.objects.filter(order=the_order)

    return render (request, 'order_success.html', {'order_details': the_order,
                                                   'bought_items': bought_items})



def single_orderPDF(request):
    """
    View function: download user order as pdf file
    :param request: Http request
    :return: Pdf file if successful
    """

    bought_items = None
    order_details = None


    if 'order_ID' in request.session:


        try:
            order_details = Order.objects.get(id=int(request.session['order_ID']))
        except:
            order_details = None
    bought_items = OrderItems.objects.filter(order=order_details)

    if not bought_items == None:
        the_report = PDFGenerator(request,order_details, bought_items)
        return the_report.download_user_order()



def check_sess(request):
    return HttpResponse('Order not successful')


#******VOUGE PAY integration views

def make_payment1(request):
    """
    View function: To process payment via 'Vouge Payment' API
    :param request: Http request
    :return: redirect: success url, failure url,; render: vouge payment form
    """
    current_order = create_new_order(request)
    customer_name = current_order.get_buyer_firstname() + ' ' + current_order.get_buyer_lastname()

    success_url = request.session['domain'] + '/order/show_receipt/' + str(current_order.pk) + '/'# to show reciept page after successful payment
    failure_url = request.session['domain'] + '/order/failure/'
    notify_url = request.session['domain'] + '/order/notify/'
    memo = 'order for ' + current_order.get_buyer_firstname() +  ': ' + str(current_order.get_order_date() )

    return render(request, 'vouge-payment.html', {'order': current_order,
                                                  'success': success_url,
                                                  'fail': failure_url,
                                                  'notify': notify_url,
                                                  'memo': memo,
                                                  'customer_name': customer_name
                                                  })

def show_order_receipt1(request,order_id):
    """
    View function: show order confirmation page for Vouge payment
    :param request:
    :param the_order:
    :return:
    """
    bought_items=None
    the_order = None


    try:
        the_order = Order.objects.get(id= int(order_id))
    except:
        the_order = None

    send_order_confirmation_email(request, the_order)

    bought_items = OrderItems.objects.filter(order=the_order)

    return render (request, 'order_success.html', {'order_details': the_order,
                                                   'bought_items': bought_items})




def send_order_confirmation_email(request, the_order):
    """
    View function: sends order confirmantion email 
    :param request: Http request
    :param the_order: the new order object
    :return: 
    """

    bought_items = OrderItems.objects.filter(order=the_order)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    pdf_obj = PDFGenerator(request,the_order, bought_items)
    document = pdf_obj.user_order_pdf()

    doc.build(document)
    pdf = buffer.getvalue()
    buffer.close()

    subject = 'Order confirmation - Market woman'
    message = 'Hi ' + the_order.get_buyer_firstname() + ',\n\n' \
              'This is a confirmation email for your order detailed below:\n' \
              '     Customer name: ' + the_order.get_buyer_firstname() + ' ' + the_order.get_buyer_lastname() + '\n' \
              '     Delivery date: ' + str(the_order.get_delivery_date()) + '\n' \
              '     Delivery address ' + the_order.get_delivery_addr() + '\n' \
              '     Order date: ' + str(the_order.get_order_date()) + '\n\n' \
              'Find attached to this email the detailed order reciept\n\n' \
                                                        'MarketWomanPH'
    customer_email = the_order.get_buyer_email()

    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [customer_email]
            )

    filename = 'order_' + the_order.get_buyer_firstname() + '_' +str(the_order.get_order_date()) + '.pdf'
    email.attach(filename, pdf,'application/pdf')
    email.send(
        fail_silently=False
    )

    return


