from database.databaseManager import DatabaseManager

class AdManagerSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def get_advertisements_by_user(self, user_id):
        try:
            query = """
            SELECT a.*, m.title, m.director, m.runtime, m.genre, m.release_date, m.description, m.rating, m.booking_rate, m.price
            FROM Advertisements a
            JOIN Movies m ON a.movie_id = m.movie_id
            WHERE a.user_id = %s;
            """
            results, columns = self.con.execute_query(query, (user_id,))
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Failed to fetch advertisements for user ID {user_id}:", e)
            return []
        
    def get_movies(self):
        # Movies 테이블을 조회하여 영화 제목을 가져옴
        result, columns = self.con.execute_query("""
            SELECT DISTINCT title, movie_id 
            FROM Movies
            ORDER BY movie_id ASC;
        """)
        return result        
        
    def add_advertisement(self, user_id, movie_id):
        try:
            # 해당 사용자가 이미 해당 movie_id에 대한 광고를 등록했는지 확인
            check_query = """
            SELECT * FROM Advertisements WHERE user_id = %s AND movie_id = %s;
            """
            existing_ads, _ = self.con.execute_query(check_query, (user_id, movie_id))

            if existing_ads:
                # 이미 광고가 있으면 예외 발생
                raise Exception("이미 해당 영화의 광고가 등록되어 있습니다.")
            else:
                # 광고가 없으면 새로 추가
                insert_query = """
                INSERT INTO Advertisements (user_id, movie_id) VALUES (%s, %s);
                """
                self.con.execute_action_query(insert_query, (user_id, movie_id))
                print(f"Advertisement added successfully for user ID {user_id} and movie ID {movie_id}.")
        except Exception as e:
            print(e)
            raise e

    def delete_advertisement(self, advertisement_id):
        try:
            delete_query = """
            DELETE FROM Advertisements WHERE advertisement_id = %s;
            """
            self.con.execute_action_query(delete_query, (advertisement_id,))
            print(f"Advertisement for advertisement ID {advertisement_id} deleted successfully.")
        except Exception as e:
            print("Failed to delete advertisement:", e)
            raise e

    def close(self):
        self.con.close()