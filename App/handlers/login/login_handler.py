from passlib.hash import sha256_crypt
from flask import request
from App.database_py_files.sql_file_reader_runtime import SqlFileRuntimeReader


class LoginHandler:
    def __init__(self, cursor):
        self.cursor = cursor

    @staticmethod
    def verify_password(db_password, form_password):

        verified_password = sha256_crypt.verify(form_password, db_password)
        if verified_password:
            return True
        return False

    def login(self):
        db_password, form_password = self.get_db_password()
        if db_password and form_password:
            verified_password = self.verify_password(form_password, db_password)
            if verified_password:
                return True
            return False
        return False

    @staticmethod
    def get_form_inputs():

        form_email = request.form["email"]
        form_password = request.form["password"]
        return form_email, form_password

    def get_db_password(self, sql_file_reader=SqlFileRuntimeReader):

        form_email, form_password = self.get_form_inputs()
        sql_file_reader = sql_file_reader()
        self.cursor.execute(
            sql_file_reader.read_get_user_password(),
            (form_email,),
        )
        query_result = self.cursor.fetchone()
        if query_result:
            db_password = query_result[0]
            return db_password, form_password
        return False