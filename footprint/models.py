from django.db import models

# Create your models here.
class Product_details(models.Model):

    choices = [
        ('Vegetables','VEGETABLES'),
        ('Pulses','PULSES'),
        ("OilCrops",'OILCROPS'),
        ('Cereals','CEREALS'),
        ('Stimulantas','STIMULANTAS'),
        ('Spices','SPICES'),
        ('Fibres','FIBRES'),
        ('Fodder Crops','FODDER CROPS'),
        ('Nuts','NUTS'),
        ('Roots','ROOTS'),
        ('Sugar Crops','SUGAR CROPS'),
        ('Others','OTHERS')
        
    ]
    product_name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1)
    product_category = models.CharField(max_length=25,choices=choices)



    

    
