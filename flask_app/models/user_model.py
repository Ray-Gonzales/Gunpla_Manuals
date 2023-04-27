from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

PW_REGEX = re.compile(r'^(?=[A-Za-z0-9@#$%^&+!=]+$)^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%^&+!=])(?=.{8,}).*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:
    db = "gunpla_manual"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.manuals = []
        
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s );"
        return connectToMySQL(cls.db).query_db( query, data )
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        user_account = []
        for user in results:
            user_account.append( cls(user) )
        return user_account
    
    @classmethod
    def get_one_user_id(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {"id":data})
        return cls(results[0])
    
    @classmethod
    def get_one_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s , last_name = %(last_name)s , email = %(email)s , password = %(password)s WHERE id = %(id)s "
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def delete(cls,id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,{"id": id})
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(Users.db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters." , 'registration')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters." , 'registration')
            is_valid = False
        if len(user['email']) < 2:
            flash("Email must be valid!", 'registration')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Email must be valid!", 'registration')
            is_valid = False
        if len(results) >= 1:
            flash("You already have an account!", 'registration')
            is_valid = False
        if len(user['password']) < 8:            
            flash("Password must be at least 8 characters long. A combination of uppercase letters, lowercase letters, numbers, and symbols.", 'registration')
            is_valid = False
        elif not PW_REGEX.match(user['password']):
            flash("Password must be at least 8 characters long. A combination of uppercase letters, lowercase letters, numbers, and symbols.", 'registration')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password does not match!" , 'registration')
        return is_valid