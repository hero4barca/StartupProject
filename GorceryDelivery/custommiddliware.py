


from .models import Shop
from django.utils.deprecation import MiddlewareMixin

class ShopSessionsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
            function: creates sessions for shop data
            :param request:
            :return:
            """

        if 'domain' not in request.session:

            shop_details = None
            try:
                shop_details = Shop.objects.get(shop_name='market_woman')
            except:
                pass

            if not shop_details == None:
                request.session['shop_name'] = shop_details.get_name()
                request.session['shop_email'] = shop_details.get_email()
                request.session['shop_phoneNo'] = shop_details.get_phoneNo()
                request.session['shop_address'] = shop_details.get_address()
                request.session['domain'] = shop_details.get_domain()
                


                if not shop_details.get_alt_phoneNO() == None:
                    request.session['shop_phoneNo_2'] = shop_details.get_alt_phoneNO()