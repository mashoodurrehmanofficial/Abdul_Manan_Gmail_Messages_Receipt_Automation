import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), 'Django_Project'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Project.settings")
import django,time
from django.conf import settings
django.setup()
from Django_App.models import *
from mail_handler import getEmails
from datetime import datetime
try:
    from apis import TodayReportApi
    from data import  parameters
except:
    from .apis import TodayReportApi
    from .data import  parameters
    
    
    
while True:
    getEmails()
    TodayReportApi()
    print("-> Waiting") 
    for remaining in range(parameters.wait_to_search_for_new_messages, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
        # sys.stdout.flush()
        time.sleep(1)
    print('\n')

 
 
# print(db_time>current_time_object)
