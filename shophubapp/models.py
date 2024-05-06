from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class console(models.Model):
    name = models.CharField(max_length=50, verbose_name='Console Name')
    price = models.FloatField()
    pdetails = models.CharField(max_length=500, verbose_name='Product Details')
    CAT = ((1, 'PS5'), (2, 'Xbox'), (3, 'Nintendo Switch'), (4,'PS4'))
    cat = models.IntegerField(verbose_name = 'Product Category', choices = CAT)
    is_active = models.BooleanField(default=True, verbose_name = 'Availability')
    pimage = models.ImageField(upload_to='image')

    def __str__(self):              #Show the names of products in the admin panle db
        return self.name


class game(models.Model):
    title  = models.CharField(max_length=100, verbose_name='Game Title')
    price = models.FloatField()
    gdetails = models.CharField(max_length=500, verbose_name='Game Details')
    PLTFRM = ((1, 'PS'), (2, 'Xbox'), (3, 'Switch'), (4, 'PC'))
    pltfrm = models.IntegerField(verbose_name='Platform', choices=PLTFRM)
    is_active = models.BooleanField(default = True,  verbose_name= 'Availability')
    gimage = models.ImageField(upload_to='image')

    def __str__(self):
        return self.title 

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    itype = models.CharField(max_length=50)
    itid = models.IntegerField()
    qty = models.IntegerField(default = 1)

class Order(models.Model):
    order_id = models.CharField(max_length = 50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column= 'uid')
    itype = models.CharField(max_length=50)
    itid = models.IntegerField()
    qty = models.IntegerField(default = 1)
