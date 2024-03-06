import psycopg2
from psycopg2 import IntegrityError
from database.databaseManager import DatabaseManager
import hashlib

# 로그인 클래스
class LoginSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()
    
    # 회원가입 수행
    def create_user(self, name, email, password, phone=None, role=None):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            columns = ['name', 'email', 'hashed_password']
            values = [name, email, hashed_password]
            placeholders = ['%s', '%s', '%s']

            if phone is not None:
                columns.append('phone_number')
                values.append(phone)
                placeholders.append('%s')

            if role is not None:
                columns.append('user_role')
                values.append(role)
                placeholders.append('%s')
            
            self.con.execute_query(
                f"INSERT INTO Users({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING user_id;",
                values
            )
            return 1
        except IntegrityError:
            return 2
        except psycopg2.Error as e:
            return 3
    
    # 로그인을 수행, return 해당 user(user_id, name, email, phone_number, user_role)
    def get_user(self, email, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            result, columns = self.con.execute_query(
                "SELECT user_id, name, email, phone_number, user_role FROM Users WHERE email = %s AND hashed_password = %s;",
                (email, hashed_password)
            )
            return result
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.con.close()