from django.db import models
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  #1:Normal/9:Delete
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "category"  

class Ingredients(models.Model):
    category_id = models.IntegerField()    
    cover_pic = models.CharField(max_length=50)   
    name = models.CharField(max_length=50)
    calories = models.FloatField()    
    status = models.IntegerField(default=1)   #1:Normal/9:Delete     
    create_at = models.DateTimeField(default=datetime.now)   
    update_at = models.DateTimeField(default=datetime.now)   

    def toDict(self):
        return {'id':self.id,'cover_pic':self.cover_pic,'name':self.name,'calories':self.calories,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "ingredients"