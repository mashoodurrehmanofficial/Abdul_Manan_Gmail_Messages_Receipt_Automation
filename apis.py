import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), 'Django_Project'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Project.settings")
import django
from django.conf import settings
django.setup()
from django.db.models import Q
try:
    from .data_extractor import EXTRACT_DATA_FROM_BODY
    from .template_generator import  GENERATE_TEMPLATE_IMAGE,GENERATE_TODAY_REPORT_TEMPLATE_IMAGE
    from .data import parameters
except :
    from data_extractor import EXTRACT_DATA_FROM_BODY
    from template_generator import  GENERATE_TEMPLATE_IMAGE,GENERATE_TODAY_REPORT_TEMPLATE_IMAGE
    from data import parameters

from Django_App.models import Orders_Table,Report_Date_Log

from datetime import  datetime



def convertToFloat(val):
    try:
        val = float(str(val).replace('$',''))
        return val
    except:
        return float(0)

def singleMessageApi(message_id):
    target_message = Orders_Table.objects.filter(message_id = message_id)
    if not target_message:
        print("New Message detected having Order")
        data_ch = EXTRACT_DATA_FROM_BODY(file_path = f"email_body_received.txt",lang='chinese') 
        GENERATE_TEMPLATE_IMAGE(data_ch)
        data = EXTRACT_DATA_FROM_BODY(file_path = f"email_body_received.txt",lang='eng') 
        GENERATE_TEMPLATE_IMAGE(data)
        print(data)
        Orders_Table(
            message_id            = message_id,
            uu_menu_id            = data['uu_menu_id'],
            delivery_method       = data['delivery_method'],
            payment_method        = data['payment_method'],
            customer_name         = data['customer_name'],
            customer_phone        = data['customer_phone'],
            customer_addres       = data['customer_addres'],
            menu_orders           = data['menu_orders'],
            sub_total             = convertToFloat(data['sub_total']),
            sales_tax_838         = convertToFloat(data['sales_tax_838']),
            delivery_fee          = convertToFloat(data['delivery_fee']),
            delivery_fee_tax_838  = convertToFloat(data['delivery_fee_tax_838']),
            tip                   = convertToFloat(data['tip']),
            total                 = convertToFloat(data['total']),
            date_object           = datetime.now().date(),
        ).save()
    else:
        print("--> Message already Read !")
        return 0
        
        
def TodayReportApi():
    current_time_object =datetime.now()
    stored_date_object = Report_Date_Log.objects.filter(date_object = current_time_object)
    if not stored_date_object:
        target_date_object = datetime(current_time_object.year, current_time_object.month, current_time_object.day,parameters.hour,parameters.minutes,0,0)
        difference = abs(int(int((target_date_object - current_time_object).total_seconds())/60))
        print(difference)
        if difference<=30:
            Report_Date_Log.objects.all().delete()
            print("-----> Creating Stat Report for Today") 
            Report_Date_Log(date_object = current_time_object).save()
 

            today_date = datetime.now().date()
            today_data = list(Orders_Table.objects.filter(date_object = today_date).values())
            today_sub_total             =   round(sum([x['sub_total'] for x in today_data]),2)
            today_tip                   =   round(sum([x['tip'] for x in today_data]),2)
            today_total                 =   round(sum([x['total'] for x in today_data]),2)
            
            total_cash = Orders_Table.objects.filter(date_object = today_date,payment_method__icontains='cash').values()
            total_cash = round(sum([x['total'] for x in total_cash]),2)
 
 
            total_online_payments = Orders_Table.objects.filter(~Q(payment_method__icontains='CASH')).values()
            total_online_payments = round(sum([x['total'] for x in total_online_payments]),2)
            data = {
                # 'sub_total'             : today_sub_total,
                'total_cash'            : total_cash,
                'total_online_payments' : total_online_payments,
                'tip'                   : today_tip,
                'overall_total'         : today_total,
            }
            for x in data:
                data[x] = '$' + str(data[x])
                
                
            print("--> Today Report Stats:\n", data)
            GENERATE_TODAY_REPORT_TEMPLATE_IMAGE(data)


if __name__=="__main__":
    TodayReportApi()