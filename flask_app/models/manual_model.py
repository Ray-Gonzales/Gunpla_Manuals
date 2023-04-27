from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import Users
import pprint

class Manuals:
    db = "gunpla_manual"
    def __init__( self , data ):
        self.id = data['id']
        self.kit_name = data['kit_name']
        self.series = data['series']
        self.release_year = data['release_year']
        self.ins_manual = data['ins_manual']
        self.exclusive = data['exclusive']
        self.cover_art = data['cover_art']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO manuals ( kit_name , series , release_year , ins_manual, exclusive, cover_art, user_id) VALUES ( %(kit_name)s , %(series)s , %(release_year)s , %(ins_manual)s , %(exclusive)s , %(cover_art)s , %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all_info(cls):
        query = "SELECT * FROM manuals JOIN users ON users.id = manuals.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        pprint.pprint(results, sort_dicts=False)
        manual_list = []
        for row in results:
            manual = cls(row)
            user_data = {
            "id" : row['id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
            }
            manual.user = Users(user_data)
            manual_list.append(manual)
        return manual_list
        
    @classmethod
    def search(cls, manual):
        query = "SELECT * FROM gunpla_manual.manuals WHERE MATCH (kit_name, series) AGAINST ('{}') ORDER BY id ASC".format(manual)
        results = connectToMySQL(cls.db).query_db(query)
        manual_list = []
        for row in results:
            manual = cls(row)
            manual_list.append(manual)
        return manual_list
        
    @classmethod
    def get_one_kit(cls, id):
        query  = "SELECT * FROM manuals JOIN users ON users.id = user_id WHERE manuals.id =  %(id)s;"
        data = {'id':id}
        results = connectToMySQL(cls.db).query_db(query, data)
        pprint.pprint(results, sort_dicts=False)
        manual_list = []
        for row in results:
            manual = cls(row)
            user_data = {
            "id" : row['id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
            }
            manual.user = Users(user_data)
            manual_list.append(manual)
        return manual_list
        
    @classmethod
    def update(cls, data ):
        query = "UPDATE manuals SET kit_name = %(kit_name)s, series = %(series)s, release_year = %(release_year)s, ins_manual = %(ins_manual)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )
        
    @classmethod
    def delete(cls,id):
        query  = "DELETE FROM manuals WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,{"id": id})
    
    
    @staticmethod
    def validate_manual(gundam_manual):
        is_valid = True
        if len(gundam_manual['kit_name']) < 3:
            flash("Kit Name must be at least 3 characters." , 'content')
            is_valid = False
        if len(gundam_manual['series']) < 3:
            flash("Series must be at least 3 characters.", 'content')
            is_valid = False
        return is_valid