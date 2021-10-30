import re 
try:
  from template_generator import  GENERATE_TEMPLATE_IMAGE
except:
  from template_generator import  GENERATE_TEMPLATE_IMAGE
  
  
def remove_chinese(string): 
  en_list = re.findall(u'[^\u4E00-\u9FA5]', string)
  for c in string:
      if c not in en_list: 
          string = string.replace(c, '') 
  return string
  
    
def extract_chinese(string):
  chinese = ''
  en_list = re.findall(u'[^\u4E00-\u9FA5]', string)
  for c in string:
      if c not in en_list:
          chinese = chinese+c
          string = string.replace(c, '') 
  return chinese
  
  
   
  
message_body = """
===new order===



Order no: 391469661

Accepted at: Thursday, Oct 28, 2021, 6:54 PM



Type: DELIVERY

Delivery time: Thursday, Oct 28, 2021, 7:39 PM

Payment method: PAID ONLINE 

SUBTOTAL $37.48

Sales tax (8.38%):  $3.14

DELIVERY FEE $4.55

DELIVERY FEE TAX (8.38%): $0.38

TIP $4.10

TOTAL: $49.65



===client info===



Name: TaSheedah Clark

Email: iinfinitedreams1214@gmail.com

Phone: +17027138802

Address: 5830 Barbosa Dr unit 2, 89031, N Las Vegas

IP: 72.193.51.79



===items===



Item: 1 x WONTON SOUP 馄饨汤 $2.75

Size - CUP 

--------------------------



Item: 1 x ORANGE CHICKEN 橙皮鸡 $11.45

Modification  other - No Spicy 不辣 

Modification  other - Egg Fried Rice instead Steam Rice 换炒饭 (+$1.50)

--------------------------



Item: 2 x FRIED CHICKEN WINGS (8) 炸鸡翅 $17.50

--------------------------



Item: 1 x CHICKEN CHOW MEIN 鸡炒面 $7.75

--------------------------



                            Promo deal:  5% Off Your 1st Order -$1.97

--------------------------



===end of order===

"""
# 

 

def EXTRACT_DATA_FROM_BODY(file_path,body=None,lang='eng'):
  body = open(file_path,'r',encoding='utf-8').read() 
  body = body.split('\n')
  body = [x for x in body if str(x) != ''] 
  
  client_info_start_index = [index for index,x in enumerate(body) if '===client info===' in x][0]
  items_start_index = [index for index,x in enumerate(body) if '===items===' in x][0]


  accepted_date = [x.replace('Accepted ','').replace('at:','').replace('on:','').strip() for x in body if 'Accepted'.lower() in str(x).lower()]
  order_number = [x.split(':')[-1].strip() for x in body if x.lower().startswith('Order'.lower())]
  delivery_method = [x.replace('Type:','').strip() for x in body if x.startswith('Type:')]
  payment_method = [x.replace('Payment method:','').strip() for x in body if x.startswith('Payment method')]
  
  
  
  customer_info = body[client_info_start_index:items_start_index]
  customer_name = [x.replace('Name:', '').strip() for x in body if x.startswith('Name')]
  customer_email = [x.replace('Email:', '').strip() for x in body if x.startswith('Email')]
  customer_phone = [x.replace('Phone:', '').strip() for x in body if x.startswith('Phone')]
  customer_address = [x.replace('Address:', '').strip() for x in body if x.startswith('Address')]
  customer_ip = [x.replace('IP:', '').strip() for x in body if x.startswith('IP:')]
  
  
  order_table = body[items_start_index+1:]
  order_table = [x.replace('Item:', '') for x in order_table if '--------------' not in x and 'end of order' not in x and not 'Promo deal:' in x]
  
  menu_orders = []
  index = 0
  for line in order_table:
      order_section = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
      if len(order_section)>=2:
        quantity = str(order_section[0])+'x'
        price    = '$'+str(order_section[-1])
        menu_orders.append(
          {
            'quantity': quantity,
            "price"   : price,
            "items"   : [line.replace(quantity,'').replace(price,'').strip()]
          }
        )
        index += 1
      else:
        try:  menu_orders[index-1]['items'].append(line.strip())
        except :  menu_orders[index]['items'].append(line.strip())
          
  for order_index,order in enumerate(menu_orders):
    for item_index,item in enumerate(order['items']):
      if lang=='eng':
        menu_orders[order_index]['items'][item_index] = remove_chinese( menu_orders[order_index]['items'][item_index])
      else :                                                                  
        menu_orders[order_index]['items'][item_index] = extract_chinese( menu_orders[order_index]['items'][item_index])

      menu_orders[order_index]['items'][item_index] = menu_orders[order_index]['items'][item_index].replace(order['quantity'].replace('x', ' x'),'').strip()
  
  # # Recepit Totals
  sub_total             = [x.replace('SUBTOTAL','').strip() for x in body if 'SUBTOTAL' in x]
  sales_tax_838         = [x.replace('Sales tax (8.38%):','').strip() for x in body if 'Sales tax (8.38%)' in x]
  delivery_fee          = [x.replace('DELIVERY FEE','').strip() for x in body if 'DELIVERY FEE' in x]
  delivery_fee_tax_838  = [x.replace('DELIVERY FEE TAX (8.38%):','').strip() for x in body if 'DELIVERY FEE TAX (8.38%):' in x]
  tip                   = [x.replace('TIP:','').strip() for x in body if 'TIP' in x]
  total                 = [x.replace('TOTAL:','').strip() for x in body if str(x).startswith( 'TOTAL' )]
 

  data = {
    "uu_menu_id"            : order_number,
    "delivery_method"       : delivery_method,
    "payment_method"        : payment_method,
    "customer_name"         : customer_name,
    "customer_phone"        : customer_phone,
    'customer_addres'       : customer_address,
    'menu_orders'           : menu_orders,
    'sub_total'             : sub_total,
    'sales_tax_838'         : sales_tax_838,
    'delivery_fee'          : delivery_fee,
    'delivery_fee_tax_838'  : delivery_fee_tax_838,
    'tip'                   : tip,
    'total'                 : total,
    "accepted_date"         : accepted_date,
    "lang"                  : lang
  }
  
  for key in data:
    if type(data[key]) is list and key!='menu_orders':
      if len(data[key])>0:
        # print(data[key])
        data[key] = data[key][0]
      else:
        data[key] = 'N/A'
      # pass
    
  
  return data













if __name__=="__main__":
  # message_body = open('email_body_40.txt','r',encoding='utf-8').read()
  # data = EXTRACT_DATA_FROM_BODY(message_body)
  data = EXTRACT_DATA_FROM_BODY(file_path='email_body_received.txt',lang='ch')
  # print(data)
  GENERATE_TEMPLATE_IMAGE(data)
 
    
  # for x,y in data.items():
  #   print(x, "--> ",y)
  
 