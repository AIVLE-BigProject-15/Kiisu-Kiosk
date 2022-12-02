from django.db import models

class Model(models.Model):
    MODEL_CHOICE = (('CNN', "cnn"), 
                    ('DNN', 'dnn'), 
                    ('RandomForest', 'rf'), 
                    ('KNN', 'knn'), 
                    ('SGD', 'sgd'), 
                    ('XGB', 'xgb'))

    model = models.FileField(upload_to= 'model/', blank=True)
    type = models.CharField(max_length=12, choices=MODEL_CHOICE, default='CNN')
    version = models.CharField(max_length=10)
    comment = models.CharField(default= " ", max_length=300)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.version
    
class Menu(models.Model):
    class Meta:
        ordering = ['-id']
        
    title = models.CharField('메뉴명', max_length=250, unique=True)
    price = models.IntegerField('가격', default='0')
    image = models.ImageField(upload_to='menu/images/', null=False)
    
    
    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    calorie = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    AGE_GROUP = (('youth', "Youth"), 
                    ('middle', 'Middle-Aged'), 
                    ('senior', 'Senior'))
    class Meta:
        ordering = ['-id']
        
    image = models.ImageField(upload_to='face/images/', null=False)
    created = models.DateField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    age_group = models.CharField(max_length=12, choices=AGE_GROUP, default=0)
    version = models.ForeignKey(Model, related_name='versionR', on_delete=models.CASCADE, db_column='version', default=0)

    
class Order(models.Model):
    class Meta:
        ordering = ['-id']
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )    
    created = models.DateField(auto_now_add=True) 

