from App.database_py_files.sql_file_reader_runtime import SqlFileRuntimeReader
from passlib.hash import sha256_crypt
from flask import flash


class RegisterHandler:
    def __init__(self, form, cursor, sql_reader=SqlFileRuntimeReader):
        self.form = form
        self.cursor = cursor
        self.sql_reader = sql_reader()

    @staticmethod
    def params_register(email, password_user):
        params = {"_email": email, "_password": password_user}
        return params

    def register_user(self):

        email = self.form.email.data
        password = sha256_crypt.encrypt(self.form.password.data)
        sql_insert = self.sql_reader.read_register_user()
        params_register = self.params_register(email, password)
        self.cursor.execute(sql_insert, params_register)
        flash("Thanks for registering!", "success")
