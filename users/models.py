from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 50) 
    nickname = models.CharField(max_length = 50)    
    password_hash = models.CharField(max_length = 100) 
    password_salt = models.CharField(max_length = 50)    
    status = models.IntegerField(default = 1)    #1:Normal/9:Delete
    create_at = models.DateTimeField(default = datetime.now) 
    update_at = models.DateTimeField(default = datetime.now) 

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,
        'password_hash':self.password_hash,'password_salt':self.password_salt,
        'status':self.status,
        'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"

