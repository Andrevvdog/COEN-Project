# COEN-Project

This cooking robot recipe manager is a web application based on Django Framework and using MySQL as backend database.


# Software Requirements:

python        3.7  
django        3.2.14  
mysql         8.0.30  
pymysql       1.0.2  
captcha       0.4  
numpy         1.21.6  
matplotlib    3.5.2  


# To run this application locally:

## download the project from github

git clone https://github.com/Andrevvdog/COEN-Project.git

cd COEN-Project

## download the static.zip from google drive and unzip it into the COEN-Project

google drive share link: https://drive.google.com/file/d/1HKBnBRc0LimHzq3bOhN7whBubL-3ymMg/view?usp=sharing

## create database on MySQL

mysql -uroot -p  // the password should be aligned with settings.py under COEN-Project/reciperobot

create database rkdb4;

exit

## run Django application

cd COEN-Project

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

## open a web broswer to check

http://localhost:8000/users
