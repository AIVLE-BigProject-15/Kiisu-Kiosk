from django.db import models
from django_resized import ResizedImageField


class Model(models.Model):
    model = models.FileField(upload_to= 'model/', blank=True)
    version = models.CharField(max_length=10)
    comment = models.CharField(default= " ", max_length=300)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.version
    
class Menu(models.Model):
    BEVERAGE_TYPE = (('hot_coffee', "Hot Coffee"), 
                    ('ice_coffee', 'Ice Coffee'), 
                    ('non_coffee', 'Non Coffee'),
                    ('smoothie', 'Smoothie'),
                    ('bread', 'Bread'),
                    ('cookie', 'Cookie'),
                    )
    class Meta:
        ordering = ['-id']
        
    title = models.CharField('메뉴명', max_length=250, unique=True)
    en_title = models.CharField(max_length=250, default="")
    
    price = models.IntegerField('가격', default='0')
    image = models.ImageField(upload_to='menu/images/', null=False)
    
    desc = models.CharField(max_length=250, default="")
    type = models.CharField(max_length=20, choices=BEVERAGE_TYPE, default=0)
    is_best_menu = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    calorie = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    AGE_GROUP = [(f'{i}0', f'{i}0대') for i in range(1, 6)]
    AGE_GROUP.append(('60', '60대 이상'))
    
    AGE_GROUP = tuple(AGE_GROUP)

    class Meta:
        ordering = ['-id']
        
    created = models.DateField(auto_now_add=True) 
    age_group = models.CharField(max_length=12, choices=AGE_GROUP, default=0)
    
class Order(models.Model):
    class Meta:
        ordering = ['-id']
    
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.IntegerField('수량', default=0)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True
    )    
    created = models.DateField(auto_now_add=True) 


