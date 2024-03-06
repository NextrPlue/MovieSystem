import psycopg2
from psycopg2 import IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'dbname': 'db_movie',
            'user': 'du_movie',
            'password': '4510471',
            'host': '::1',
            'port': '4510'
        }
        self.con = None

    def connect(self):
        try:
            self.con = psycopg2.connect(**self.db_config)
            print("Database connection established.")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def close(self):
        if self.con is not None:
            self.con.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            with self.con.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]  # 컬럼 이름 가져오기
                self.con.commit()
                return results, columns  # 결과와 컬럼 이름을 함께 반환
        except IntegrityError as e:
            self.con.rollback()
            raise e
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.con.rollback()
            raise 

    def execute_action_query(self, query, params=None):
        try:
            with self.con.cursor() as cursor:
                cursor.execute(query, params)
                self.con.commit()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.con.rollback()
            raise e

    def set_isolation_level_read_committed(self):
        try:
            self.con.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        except psycopg2.Error as e:
            print(f"Error executing set isolation level: {e}")
            self.con.rollback()
            raise e