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

class Recipes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipebook = models.ForeignKey(RecipeBook,on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredients)

    name = models.CharField(max_length=255)
    cover_pic = models.CharField(max_length=255)
    total_calories = models.FloatField(default=0) 
    rate = models.FloatField(default=1)
    methods = models.CharField(max_length=1024)
    cooking_time = models.FloatField()
    keywords = models.CharField(max_length=255)

    status = models.IntegerField(default=1)   #1:Normal/9:Delete  
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'user_id':self.user,'recipebook_id':self.recipebook,'ingredients_id':self.ingredients,
        'name':self.name,'cover_pic':self.cover_pic,'total_calories':self.total_calories,'rate':self.rate,'methods':self.methods,'cooking_time':self.cooking_time,'keywords':self.keywords,
        'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    class Meta:
        db_table = "recipes"


