from database.databaseManager import DatabaseManager
from .movieBookingSystem import MovieBookingSystem

class MovieManagementSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def get_all_movies(self):
        query = "SELECT * FROM Movies ORDER BY movie_id ASC;"
        try:
            results, columns = self.con.execute_query(query)
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("Error fetching user data:", e)
            return []

    def add_movie(self, title, director, runtime, genre, release_date, description, price):
        try:
            rating = 0
            booking_rate = 0

            self.con.execute_action_query(
                "INSERT INTO Movies (title, director, runtime, genre, release_date, description, rating, booking_rate, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (title, director, runtime, genre, release_date, description, rating, booking_rate, price)
            )
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print("Failed to add movie:", e)
            raise e

    def delete_movie(self, movie_id):
        try:
            self.preprocessing(movie_id)
            # Movies 테이블에서 해당 영화 삭제
            self.con.execute_action_query(
                "DELETE FROM Movies WHERE movie_id = %s;",
                (movie_id,)
            )
            system = MovieBookingSystem()
            system.update_booking_rate()
            system.close()
            print(f"Movie with ID {movie_id} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete movie with ID {movie_id}:", e)
            raise e
        
    def update_movie(self, movie_id, title, director, runtime, genre, release_date, description, price):
        try:
            self.preprocessing(movie_id)
            # 영화 정보 업데이트
            self.con.execute_action_query(
                "UPDATE Movies SET title = %s, director = %s, runtime = %s, genre = %s, release_date = %s, description = %s, price = %s WHERE movie_id = %s;",
                (title, director, runtime, genre, release_date, description, price, movie_id)
            )
            system = MovieBookingSystem()
            system.update_booking_rate()
            system.close()
            print(f"Movie with ID {movie_id} updated successfully.")
        except Exception as e:
            print(f"Failed to update movie with ID {movie_id}:", e)
            raise e

    def preprocessing(self, movie_id):
        try:
            # Screenings 테이블에서 해당 영화의 모든 상영 ID 가져오기
            screenings, _ = self.con.execute_query(
                "SELECT screening_id FROM Screenings WHERE movie_id = %s;",
                (movie_id,)
            )

            self.con.execute_action_query(
                "DELETE FROM Advertisements WHERE movie_id = %s;",
                (movie_id,)
            )

            self.con.execute_action_query(
                "DELETE FROM Ratings WHERE movie_id = %s;",
                (movie_id,)
            )
            
            # 각 상영에 대한 예약 및 좌석 정보 삭제
            for screening in screenings:
                screening_id = screening[0]

                # Reservations 테이블에서 해당 상영에 대한 예약 삭제
                self.con.execute_action_query(
                    "DELETE FROM Reservations WHERE screening_id = %s;",
                    (screening_id,)
                )

                # Seats 테이블에서 해당 상영의 좌석 삭제
                self.con.execute_action_query(
                    "DELETE FROM Seats WHERE screening_id = %s;",
                    (screening_id,)
                )

            # Screenings 테이블에서 해당 영화에 대한 상영 정보 삭제
            self.con.execute_action_query(
                "DELETE FROM Screenings WHERE movie_id = %s;",
                (movie_id,)
            )
        except Exception as e:
            print(f"Failed to preprocessing movie with ID {movie_id}:", e)
            raise e


    def close(self):
        self.con.close()