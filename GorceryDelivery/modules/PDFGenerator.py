import reportlab

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import  TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter

from GorceryDelivery.models import Order,OrderItems
from django.http import HttpResponse

class PDFGenerator():

    def __init__ (self, request, order_details, bought_items):

        self.order_details = order_details
        self.bought_items = bought_items
        self.request = request


    def user_order_pdf(self):

        logo_style = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=32,
            textColor = colors.green,
            alignment= TA_CENTER)

        heading_style = ParagraphStyle(
            name='Normal',
            fontName= 'Helvetica',
            fontSize= 15,
            alignment= TA_CENTER
        )

        details_style = ParagraphStyle(
            name='Normal',
            fontName= 'Helvetica',
            fontSize= 12
        )

        lastLinestyle = ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8.5)

        styles = getSampleStyleSheet()


        doc_text = []

        #company name line
        company_line = Paragraph('Market Woman', logo_style)
        time_of_order = self.order_details.get_order_time()
        time_of_order = time_of_order.strftime("%H:%M:%S")
        order_title_line = Paragraph('Order Receipt, date: '  + str(self.order_details.get_order_date()) + ' ' +time_of_order, heading_style)

        doc_text.append(company_line)
        doc_text.append(Spacer(1, 0.35 * inch))
        doc_text.append(order_title_line)
        doc_text.append(Spacer(1, 0.23 * inch))

        #order details
        if self.order_details.get_buyer_gender() == 'male':
            gender = '(Mr.)'
        else:
            gender = '(Mrs.)'

        customer_name = 'Customer Name: ' + self.order_details.get_buyer_firstname() + ' ' + self.order_details.get_buyer_lastname() + gender
        details_line_1 = Paragraph(customer_name, details_style)
        details_line_2 = Paragraph('Email: ' + self.order_details.get_buyer_email(), details_style)
        details_line_3 = Paragraph('Tel No: ' + self.order_details.get_buyer_phone_no(), details_style)
        details_line_4 = Paragraph('Order delivery date: ' + str(self.order_details.get_delivery_date()), details_style)
        details_line_5 = Paragraph('Delivery Address: ' + self.order_details.get_delivery_addr(), details_style)
        #details_line_6 = Paragraph('Order date: ' + str(self.order_details.get_order_date()) + ':' + str(self.order_details.get_order_time()), details_style)

        doc_text.append(details_line_1)
        doc_text.append(Spacer(1, 0.085 * inch))
        doc_text.append(details_line_2)
        doc_text.append(Spacer(1, 0.085 * inch))
        doc_text.append(details_line_3)
        doc_text.append(Spacer(1, 0.085 * inch))
        doc_text.append(details_line_4)
        doc_text.append(Spacer(1, 0.085 * inch))
        doc_text.append(details_line_5)
        #doc_text.append(Spacer(1, 0.085 * inch))
        #doc_text.append(details_line_6)
        doc_text.append(Spacer(1, 0.4 * inch))

        table_data = []

        table_thead = ['No.', 'Name(qty): description' , 'Price*qty', 'Amt(in Naira)']
        table_data.append(table_thead)

        data_row=[]
        for index, order_item in enumerate(self.bought_items):
            first_col = index+1
            second_col = order_item.get_item().get_name() + '(' + str(order_item.get_quantity()) + '): ' +order_item.get_order_item_desc()
            third_col= str(order_item.get_order_item_price()) + '*' + str(order_item.get_quantity())
            fourth_col =str(order_item.get_price_by_qty())
            data_row = [first_col, second_col, third_col, fourth_col ]
            table_data.append(data_row.copy())

        items_total = self.order_details.get_items_total()
        items_total_row = [' - ', 'items total', '', items_total ]
        table_data.append(items_total_row)

        service_charge = self.order_details.get_service_charge()
        service_charge_row = [' - ', 'service charge', '', service_charge]
        table_data.append(service_charge_row)

        final_total = self.order_details.get_order_total()
        final_total_row =[' - ', ' final total ', '', final_total]
        table_data.append(final_total_row)

        t = Table(table_data)
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1, -1), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('FONTSIZE', (0,0),(-1,-1), 12),
                               ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
                               ('FONTNAME', (0,-1), (3, -1), 'Helvetica-Bold'),
                               ('BOX',(0,-1), (3, -1), 0.25,colors.black),
                               ('BACKGROUND', (0, -1), (3, -1), colors.grey)
                               ]) )

        doc_text.append(t)


        website = self.request.session['domain']
        Tel_no = self.request.session['shop_phoneNo']
        contact_email = self.request.session['shop_email']

        last_line_text = """ This receipt is automatically generated by '""" + website + """' and serves as an official confirmation of order.
                             It is also your official proof of payment. For any complaint or enquiry, please contact us via
                              """ + contact_email + """ or by calling """ + Tel_no
        last_line_text_1 = """ ****NOTE: We will reach you via the phone number provided above to facilitate delivery. Please ensure
                                that you stay reachable via the provided contact number on the stated delivery date.\n
                                 Delivery hours: 10am - 4pm."""

        last_paragraph = Paragraph(last_line_text, lastLinestyle)
        last_paragraph_1 = Paragraph(last_line_text_1, lastLinestyle)
        doc_text.append(Spacer(1, 0.5 * inch))
        doc_text.append(last_paragraph)
        doc_text.append(Spacer(1, 0.08 * inch))
        doc_text.append(last_paragraph_1)

        return doc_text



    def download_user_order(self):

        response = HttpResponse(content_type='application/pdf')

        filename = 'order_' + str(self.order_details.get_order_date()) + '_' + str(
                self.order_details.get_order_time()) + '.pdf'
        disposition = 'attachment; filename="' + filename + '"'
        response['Content-Disposition'] = disposition
        report_pdf = self.user_order_pdf()

        doc = SimpleDocTemplate(response)

        doc.build(report_pdf)
        return response


