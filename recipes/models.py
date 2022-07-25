from django.db import models
from datetime import datetime
from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  #1:Normal/9:Delete
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "category"  

class Ingredients(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  
    cover_pic = models.CharField(max_length=50)   
    name = models.CharField(max_length=50)
    calories = models.FloatField()    
    status = models.IntegerField(default=1)   #1:Normal/9:Delete     
    create_at = models.DateTimeField(default=datetime.now)   
    update_at = models.DateTimeField(default=datetime.now)   

    def toDict(self):
        return {'id':self.id, 'category_id':self.category, 'cover_pic':self.cover_pic,'name':self.name,'calories':self.calories,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "ingredients"

class RecipeBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cover_pic = models.CharField(max_length=255)
    status = models.IntegerField(default=1)   #1:Normal/9:Delete  
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'user_id':self.user,'name':self.name,'cover_pic':self.cover_pic,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    class Meta:
        db_table = "recipebook"