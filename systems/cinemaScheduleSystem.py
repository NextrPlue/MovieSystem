from database.databaseManager import DatabaseManager
import string

class CinemaScheduleSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()
        self.con.set_isolation_level_read_committed()

    def add_screening(self, screen_id, movie_id, start_time, end_time):
        try:
            # 겹치는 상영 시간이 있는지 확인
            overlap_check_query = """
            SELECT screening_id 
            FROM Screenings 
            WHERE screen_id = %s AND NOT (
                screening_end_time <= %s OR 
                screening_start_time >= %s
            );
            """
            overlaps, _ = self.con.execute_query(overlap_check_query, (screen_id, start_time, end_time))

            if overlaps:
                raise ValueError("상영시간이 기존 상영과 겹칩니다.")

            # Screenings 테이블에 스케줄 추가
            results, _ = self.con.execute_query(
                "INSERT INTO Screenings (screen_id, movie_id, screening_start_time, screening_end_time) VALUES (%s, %s, %s, %s) RETURNING screening_id;",
                (screen_id, movie_id, start_time, end_time)
            )
            screening_id = results[0][0]

            # Seats 테이블에 좌석 추가
            self.add_seats(screen_id, screening_id, self.fetch_seat_capacity(screen_id))

            print(f"Movie ID {movie_id} scheduled in Screen {screen_id} with Screening ID {screening_id} from {start_time} to {end_time}.")
        except ValueError as e:
            print(e)
            raise e
        except Exception as e:
            print("Failed to schedule movie:", e)
            raise e

    def remove_screening(self, screening_id):
        try:
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

            # Screenings 테이블에서 해당 상영 정보 삭제
            self.con.execute_action_query(
                "DELETE FROM Screenings WHERE screening_id = %s;",
                (screening_id,)
            )

            print(f"Screening with ID {screening_id} removed successfully.")
        except Exception as e:
            print(f"Error in removing screening with ID {screening_id}: {e}")

    def fetch_seat_capacity(self, screen_id):
        result, _ = self.con.execute_query("SELECT seat_capacity FROM Screens WHERE screen_id = %s;", (screen_id,))
        return result[0][0] if result else None

    def add_seats(self, screen_id, screening_id, seat_capacity):
        rows = string.ascii_uppercase
        for seat_number in range(1, seat_capacity + 1):
            row_letter = rows[(seat_number - 1) // 10]
            seat_label = f"{row_letter}{seat_number % 10 if seat_number % 10 != 0 else 10}"
            self.con.execute_action_query(
                "INSERT INTO Seats (screen_id, screening_id, seat_number) VALUES (%s, %s, %s);",
                (screen_id, screening_id, seat_label)
            )

    def get_movies_info(self):
        query = "SELECT movie_id, title, runtime FROM Movies;"
        try:
            results, columns = self.con.execute_query(query)
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Error retrieving movie information: {e}")
            return []
        
    def get_screens_info(self):
        query = "SELECT * FROM Screens;"
        try:
            results, columns = self.con.execute_query(query)
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Error retrieving screen information: {e}")
            return []

    def get_screenings_info(self):
        query = """
        SELECT
            s.*,
            m.title
        FROM Screenings s
        LEFT JOIN Movies m ON s.movie_id = m.movie_id;
        """

        try:
            results, columns = self.con.execute_query(query)
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Error retrieving screening information: {e}")
            return []

    def close(self):
        self.con.close()