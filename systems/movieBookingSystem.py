from database.databaseManager import DatabaseManager

class MovieBookingSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()
        self.con.set_isolation_level_read_committed()

    def book_movie(self, user_id, screening_id, seat_id):
        try:
            # 좌석 예약 가능 여부 확인
            result, _ = self.con.execute_query("SELECT is_available FROM Seats WHERE seat_id = %s;", (seat_id,))
            if result[0][0]:
                # 좌석 예약
                self.con.execute_action_query(
                    "INSERT INTO Reservations(user_id, screening_id, seat_id, reservation_time, payment_status) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, TRUE);",
                    (user_id, screening_id, seat_id)
                )
                # 좌석 상태 업데이트
                self.con.execute_action_query("UPDATE Seats SET is_available = FALSE WHERE seat_id = %s;", (seat_id,))
            else:
                raise Exception("좌석이 이미 예약되어있습니다.")

            print("Movie booked successfully!")
        except Exception as e:
            print("Failed to book movie:", e)
            raise e

    def cancel_movie_booking(self, user_id, screening_id, seat_id):
        try:
            # 해당 예약 찾기
            result, columns = self.con.execute_query(
                "SELECT reservation_id FROM Reservations WHERE user_id = %s AND screening_id = %s AND seat_id = %s;",
                (user_id, screening_id, seat_id)
            )
            
            # 예약이 존재하면 취소
            if result:
                reservation = result[0]
                self.con.execute_action_query(
                    "DELETE FROM Reservations WHERE reservation_id = %s;",
                    (reservation[0],)
                )
                # 좌석 상태 업데이트
                self.con.execute_action_query(
                    "UPDATE Seats SET is_available = TRUE WHERE seat_id = %s;",
                    (seat_id,)
                )
                print("Movie booking cancelled successfully!")
                self.update_booking_rate()
            else:
                print("No such reservation found.")
        except Exception as e:
            print("Failed to cancel movie booking:", e)
            raise e
        
    def update_booking_rate(self):
        try:
            result, columns = self.con.execute_query("SELECT DISTINCT movie_id FROM Movies;")
            for i in result:
                movie_id = i[0]
                # 특정 영화의 총 예약 수
                movie_reservations, _ = self.con.execute_query(
                    "SELECT COUNT(*) FROM Reservations WHERE screening_id IN (SELECT screening_id FROM Screenings WHERE movie_id = %s);",
                    (movie_id,)
                )

                # 전체 예약 수
                total_reservations, _ = self.con.execute_query("SELECT COUNT(*) FROM Reservations;")

                # 예매율 계산 (전체 예약 대비 특정 영화 예약의 비율)
                new_booking_rate = (movie_reservations[0][0] / total_reservations[0][0]) * 100 if total_reservations[0][0] > 0 else 0

                # 예매율 업데이트
                self.con.execute_action_query(
                    "UPDATE Movies SET booking_rate = %s WHERE movie_id = %s;",
                    (new_booking_rate, movie_id,)
                )

                print(f"Updated booking rate for movie ID {movie_id} to {new_booking_rate:.2f}%.")
        except Exception as e:
            print("Failed to update booking rate:", e)

    def get_movies(self):
        # Screenings과 Movies 테이블을 조인하여 영화 제목을 가져옴
        result, columns = self.con.execute_query("""
            SELECT DISTINCT m.title, m.movie_id 
            FROM Screenings s
            JOIN Movies m ON s.movie_id = m.movie_id
            ORDER BY m.movie_id ASC;
        """)
        return result
    
    def get_times(self, movie_id):
        result, columns = self.con.execute_query("""
            SELECT DISTINCT screening_start_time 
            FROM Screenings 
            WHERE movie_id = %s;
        """, (movie_id,))
        return result

    def get_screenings(self, movie_id, start_time):
        result, columns = self.con.execute_query("""
            SELECT DISTINCT screen_id 
            FROM Screenings 
            WHERE movie_id = %s AND screening_start_time = %s;
        """, (movie_id, start_time))
        return result

    def get_screening_id(self, movie_id, start_time, screen_id):
        result, columns = self.con.execute_query("""
            SELECT screening_id 
            FROM Screenings 
            WHERE screen_id = %s AND movie_id = %s AND screening_start_time = %s;
        """, (screen_id, movie_id, start_time))
        return result
    
    def get_seats(self, screen_id, screening_id):
        result, columns = self.con.execute_query("""
            SELECT seat_id, seat_number, is_available 
            FROM Seats 
            WHERE screen_id = %s AND screening_id = %s 
            ORDER BY seat_id ASC;
        """, (screen_id, screening_id))
        return result

    def close(self):
        self.con.close()