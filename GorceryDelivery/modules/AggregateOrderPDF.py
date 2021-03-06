import reportlab

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import  TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape, A4
import re

from GorceryDelivery.models import Order,OrderItems
from django.http import HttpResponse

class AggregateOrderPDF:

    def __init__(self, nested_order_items_list, the_date):

        self.nested_items_list = nested_order_items_list
        self.the_date = the_date
        self.aggregated_order_list = []


    def compute_aggregate_list(self):

        list_by_items = []
        for order_items_list in self.nested_items_list:
            for item in order_items_list:
                list_by_items.append(item)

        #passed as sort-key to sort function
        #returns the (id) of the item ordered in the db
        def get_item_id(elem):
            return elem.get_item().id

        list_by_items.sort(key=get_item_id)
        self.aggregated_order_list = list_by_items.copy()




    def generate_PDF(self):

        logo_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=32,
            textColor=colors.green,
            alignment=TA_CENTER)

        heading_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=15,
            alignment=TA_CENTER
        )

        details_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=12
        )

        lastLinestyle = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8.5)

        styles = getSampleStyleSheet()

        doc_text = []

        # company name line
        company_line = Paragraph('Market Woman', logo_style)
        doc_title_line = Paragraph(
            'Aggregated daily order for :' + str(self.the_date),  heading_style)

        doc_text.append(company_line)
        doc_text.append(Spacer(1, 0.35 * inch))
        doc_text.append(doc_title_line)
        doc_text.append(Spacer(1, 0.23 * inch))


        table_data = []

        table_thead = ['Order No.', 'item', 'qty','item price', 'Price*qty',  'description', 'M/P']
        table_data.append(table_thead)

        data_row = []

        for order_item in self.aggregated_order_list:

            the_order = order_item.get_order()
            the_order_id = the_order.id

            the_item = order_item.get_item()
            the_item_name = the_item.get_name()


            quantity = order_item.get_quantity()

            order_item_price = order_item.get_order_item_price()

            price_by_qty = order_item.get_price_by_qty()

            the_description = order_item.get_order_item_desc()

            last_col = ''

            if order_item.get_measure():
                the_measure = order_item.get_measure()
                last_col = last_col + ' -' + the_measure.get_name() + '\n'
            if order_item.get_presentation():
                the_presentation = order_item.get_presentation()
                last_col = last_col + ' -' + the_presentation.get_name() + '\n'

            data_row = [the_order_id, the_item_name, quantity, order_item_price, price_by_qty, the_description, last_col]
            table_data.append(data_row.copy())

        t = Table(table_data)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10),
                                   ('FONTNAME', (0, 0), (6, 0), 'Helvetica-Bold'),

                                   ]))

        doc_text.append(t)



        last_line_text = """ This document is automatically generated and shows all orders for the date specified above."""

        last_paragraph = Paragraph(last_line_text, lastLinestyle)

        doc_text.append(Spacer(1, 0.5 * inch))
        doc_text.append(last_paragraph)

        return doc_text



    def download_aggregate_order(self):

        response = HttpResponse(content_type='application/pdf')

        filename =  str(self.the_date) + '_aggregate_order.pdf'
        disposition = 'attachment; filename="' + filename + '"'
        response['Content-Disposition'] = disposition
        report_pdf = self.generate_PDF()

        doc = SimpleDocTemplate(response)
        doc.pagesize = landscape(A4)

        doc.build(report_pdf)
        return response


