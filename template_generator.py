import os,uuid,time
from datetime import datetime

logo_path = os.path.join(os.getcwd(),'data','logo.png')


def GENERATE_TEMPLATE_IMAGE(data):
    css_str = """
    #table1 tbody tr td{
        text-align: center ;
        border: 3px solid rgb(41, 41, 41) !important;
    }
    #table1{
        border-collapse: collapse !important;
    }
    *{
        font-weight: bold !important;
        font-size: 30px !important;
        font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
        background-color: white;
    }



    #table2{
        border-collapse: collapse !important;
    }
    #table2   tr {
            text-align: center !important;
            border-top: 3px solid rgb(41, 41, 41) !important;
        }
        


            
    #table2 tr td:nth-child(2){
        text-align: left !important;
    }

    #table3{
        border-collapse: collapse !important;
    }
    #table3   tr {
            border-top: 3px solid rgb(41, 41, 41) !important;
        }

    """


    start_str = f"""<html>
    <head>
    <link rel="stylesheet" href="./template.css">
    </head>
    <body>
        <center style="width:550px;margin-left: 20px;" >
            <!-- Header Image -->
            <div>
                <img src="{logo_path}" alt="" width="550px" height="200px">
            </div>

            <div style="max-width:50x !important">"""


    close_str = """
            </div>


        </center>
    </body>
    </html>"""


    table1 = """ 
                <table style="width:100%" id="table1">
                    <tbody>
                        <tr>
                            <td>UU Menu</td>
                            <td>{uu_menu_id}</td>
                        </tr>
                        <tr>
                            <td>{delivery_method}</td>
                            <td>{payment_method}</td>
                        </tr>
                        <tr>
                            <td>{customer_name}</td>
                            <td>{customer_phone}</td>
                        </tr>
                    </tbody>
                </table>
    """


    address = """
    <p style="text-align: left;">
    {address}
    </p>"""


    table2_upper_part = """            <table style="width:100%" id="table2">
                    <thead>
                        <tr style="text-align:center !important">
                            <td>Qty.</td>
                            <td>Description</td>
                            <td>Amt</td>
                        </tr>
                    </thead>
                    <tbody>"""

    table2_lower_part = """                </tbody>
                </table>

                <br>"""


    table3 = """
                <br>
                <!-- Table 3 -->
                <table style="width:100%" id="table3">
                    <tbody>
                        <tr>
                            <td>Subtotal</td>
                            <td>{sub_total}</td>
                        </tr>
                        <tr>
                            <td>Sales Tax (8.38%):</td>
                            <td>{sales_tax_838}</td>
                        </tr> 
                        <tr>
                            <td>Deliver Fee </td>
                            <td>{delivery_fee}</td>
                        </tr>
                    
                        <tr>
                            <td>Deliver Fee (8.38%):</td>
                            <td>{delivery_fee_tax_838}</td>
                        </tr>
                        
                        <tr>
                            <td>Tip </td>
                            <td>{tip} 
                        </tr>
                        <tr>
                            <td>Total </td>
                            <td>{total}</td>
                        </tr>
                    </tbody>
                </table>

    """


    footer = """
    <p style="text-align: center;border-top: 3px solid rgb(41, 41, 41) !important;">
        <br>
        {accepted_date} <br>
        Thanks for your purchase!
        www.newchinacuisine.com
    </p>

    """

  
    table1 = table1.format(
        uu_menu_id=data['uu_menu_id'],
        delivery_method=data['delivery_method'],
        payment_method=data['payment_method'],
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
    )
    address = address.format(address=data['customer_addres'])

    for order in data['menu_orders']:
        tr_upper_part = f"""
      <tr>
         <td>{order['quantity']}</td>
         <td>
    """
        for items in order['items']:
            tr_upper_part += str(items) + "<div style='height:6px'></div>"

        tr_lower_part = f"""
            </td>
          <td>{order['price']}</td>
        </tr>
    """
        tr = tr_upper_part+tr_lower_part
        table2_upper_part += tr

    tabel2 = table2_upper_part + table2_lower_part

    tabele3 = table3.format(
        sub_total=data['sub_total'],
        sales_tax_838=data['sales_tax_838'],
        delivery_fee_tax_838=data['delivery_fee_tax_838'],
        delivery_fee=data['delivery_fee'],
        tip=data['tip'],
        total=data['total'],
    )

    footer = footer.format(
        accepted_date=data['accepted_date']
    )

    result = start_str+table1+address + tabel2 + tabele3 + footer + close_str
    from html2image import Html2Image
    hti = Html2Image()
    recipts_folder = 'recipts_folder'
    if os.path.exists(os.path.join(os.getcwd(),recipts_folder)):pass
    else:os.makedirs(recipts_folder)
    
    hti.output_path = recipts_folder
    
    file_name =   "recipt-"  + str(data['lang']) +'-'+ str(data['uu_menu_id']) + str(datetime.now()).replace(":",'-')  +'.png'
    hti.screenshot(html_str=result, css_str=css_str, save_as=file_name,size=(650,1800))

 

def GENERATE_TODAY_REPORT_TEMPLATE_IMAGE(data):
    css_str = """
    #table1 tbody tr td{
        text-align: center ;
        border: 3px solid rgb(41, 41, 41) !important;
    }
    #table1{
        border-collapse: collapse !important;
    }
    *{
        font-weight: bold !important;
        font-size: 30px !important;
        font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
        background-color: white;
    }



    #table2{
        border-collapse: collapse !important;
    }
    #table2   tr {
            text-align: center !important;
            border-top: 3px solid rgb(41, 41, 41) !important;
        }
        


            
    #table2 tr td:nth-child(2){
        text-align: left !important;
    }

    #table3{
        border-collapse: collapse !important;
    }
    #table3   tr {
            border-top: 3px solid rgb(41, 41, 41) !important;
        }

    """


    start_str = f"""<html>
    <head>
    <link rel="stylesheet" href="./template.css">
    </head>
    <body>
        <center style="width:550px;margin-left: 20px;" >
            <!-- Header Image -->
            <div>
                <img src="{logo_path}" alt="" width="550px" height="200px">
            </div>

            <div style="max-width:50x !important">"""


    close_str = """
            </div>


        </center>
    </body>
    </html>"""




    header = """
    <p style="text-align: center;font-wight:900"> <b> All day Stats </b> </p>"""




    table1 = """
                <br>
                <!-- Table 3 -->
                <table style="width:100%" id="table3">
                    <tbody>
                        <tr>
                            <td>Total Cash</td>
                            <td>{total_cash}</td>
                        </tr>
                        <tr>
                            <td>Total Online Payments</td>
                            <td>{total_online_payments}</td>
                        </tr> 
                     
                        
                        <tr>
                            <td>Tip </td>
                            <td>{tip} 
                        </tr>
                        <tr>
                            <td>Overall Total </td>
                            <td>{overall_total}</td>
                        </tr>
                    </tbody>
                </table>

    """


    footer = """
    <p style="text-align: center;border-top: 3px solid rgb(41, 41, 41) !important;">
        <br>
        {time_stamp} <br>
        Thanks for your purchase!
        www.newchinacuisine.com
    </p>

    """

    table1 = table1.format(
        # sub_total=data['sub_total'],
        total_cash              =   data['total_cash'], 
        total_online_payments   =   data['total_online_payments'],
        tip                     =   data['tip'],
        overall_total           =   data['overall_total'],
    )

    footer = footer.format(
        time_stamp=time.strftime('%a, %d %b %Y %H:%M:%S')
    )

    result = start_str+header  + table1 + footer + close_str
    from html2image import Html2Image
    hti = Html2Image()
    recipts_folder = 'all_day_reports'
    if os.path.exists(os.path.join(os.getcwd(),recipts_folder)):pass
    else:os.makedirs(recipts_folder)
    
    hti.output_path = recipts_folder
    
    file_name =   "report-" + str(datetime.now()).replace(":",'-')  +'.png'
    hti.screenshot(html_str=result, css_str=css_str, save_as=file_name,size=(650,1000))


#   with open("template2.html",'w',encoding="utf-8")as file:
#     file.write(str(result))
