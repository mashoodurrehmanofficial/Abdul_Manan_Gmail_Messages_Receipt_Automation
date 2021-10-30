from django.db import models
from googleapiclient import model

# Create your models here.
class Orders_Table(models.Model):
    
    message_id              = models.CharField(max_length=200,default='',blank=True,null=True)
    uu_menu_id              = models.CharField(max_length=200,default='',blank=True,null=True)
    delivery_method         = models.CharField(max_length=200,default='',blank=True,null=True)
    payment_method          = models.CharField(max_length=200,default='',blank=True,null=True)
    customer_name           = models.CharField(max_length=200,default='',blank=True,null=True)
    customer_phone          = models.CharField(max_length=200,default='',blank=True,null=True)
    customer_addres         = models.CharField(max_length=200,default='',blank=True,null=True)
    menu_orders             = models.TextField(default='',blank=True,null=True)
    
    sub_total               = models.FloatField(max_length=200,default=0,blank=True,null=True)
    sales_tax_838           = models.FloatField(max_length=200,default=0,blank=True,null=True)
    delivery_fee            = models.FloatField(max_length=200,default=0,blank=True,null=True)
    tip                     = models.FloatField(max_length=200,default=0,blank=True,null=True)
    total                   = models.FloatField(max_length=200,default=0,blank=True,null=True)
    delivery_fee_tax_838    = models.FloatField(max_length=200,default=0,blank=True,null=True)
    
    date_object             = models.DateField(blank=True,null=True)
         
 

 


class Report_Date_Log(models.Model): 
    date_object             = models.DateField(blank=True,null=True) 
         
 

