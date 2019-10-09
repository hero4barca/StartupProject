

from GorceryDelivery.models import *

class ItemsInOrder:

    def __init__(self):

        self.errors = []

    def get_errors(self):
        return self.errors


    def order_item_details(self, request):
        order_item = {}

        measures_array = []
        presentation_array = []
        index = 0

        #******From here
        # use the post value of itemID to retrieve item from db
        # compute the detailed dict

        if request.POST.get('itemID', ''):
            order_item_id = request.POST.get('itemID', '')


            try:
                item_details = Item.objects.get(id=int(order_item_id)) # retrive item by id

                order_item['name'] = item_details.get_name()
                order_item['price'] = request.POST.get('price', '')
                order_item['img'] = item_details.img.url
                order_item['description'] = item_details.get_description()
                order_item['id'] = order_item_id
                order_item['qty'] = 1


            except:
                self.errors.append('item not in db')
        else:
            self.errors.append('the item ID is not found')

        if request.POST.get('measure', ''):
            market_measures = SalesMeasure.objects.filter(item_id=int(order_item['id']))

            selected_measure = None
            for measure in market_measures:
                if request.POST.get('measure', '') == measure.get_name():
                    selected_measure = measure

            if selected_measure:
                order_item['market_measure'] = selected_measure.id
                order_item['price']= str(selected_measure.get_price()) # overide initial price with price of measure
                #update description to reflect market measure
                order_item['description'] = '\n [Measure-' + selected_measure.get_description() + '; price -' + str(selected_measure.get_price()) +']'


        if request.POST.get('presentation', ''):
            item_presentation = Presentation.objects.filter(item_id=int(order_item['id']))

            selected_presentation = None
            for presentation in item_presentation:
                if request.POST.get('presentation', '') == presentation.get_name():
                    selected_presentation = presentation


            if selected_presentation:
                order_item['presentation'] = selected_presentation.id
                order_item['description'] = order_item['description'] + '\n [Presentation: '
                #for option in presentation_array:
                order_item['description'] = order_item['description'] + selected_presentation.get_description() +']'

        if len(self.errors) > 0:
            return False
        else:
            return order_item.copy()



