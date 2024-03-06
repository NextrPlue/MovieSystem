from database.databaseManager import DatabaseManager

class ScreenManagementSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()
        self.con.set_isolation_level_read_committed()

    def add_screen(self, screen_number, seat_capacity):
        try:
            self.con.execute_action_query(
                "INSERT INTO Screens (screen_number, seat_capacity) VALUES (%s, %s);",
                (screen_number, seat_capacity)
            )
            print(f"Screen number {screen_number} with capacity {seat_capacity} added successfully.")
        except Exception as e:
            print("Failed to add screen:", e)

    def get_screens(self):
        try:
            results, columns = self.con.execute_query("SELECT * FROM Screens ORDER BY screen_number ASC;")
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("Failed to retrieve screens:", e)
            return []

    def update_screen(self, screen_id, new_screen_number, new_seat_capacity):
        try:
            # Screenings에서 해당 screen_id의 모든 screening_id 찾기
            results, columns = self.con.execute_query(
                "SELECT screening_id FROM Screenings WHERE screen_id = %s;", (screen_id,)
            )
            screenings = results

            # 해당 screening_id에 대한 Reservations 및 Seats 정보 삭제
            for screening in screenings:
                self.con.execute_action_query(
                    "DELETE FROM Reservations WHERE screening_id = %s;", (screening[0],)
                )
                self.con.execute_action_query(
                    "DELETE FROM Seats WHERE screen_id = %s AND screening_id = %s;", (screen_id, screening[0],)
                )
                self.con.execute_action_query(
                    "DELETE FROM Screenings WHERE screen_id = %s AND screening_id = %s;", (screen_id, screening[0],)
                )                

            # Screens 테이블 업데이트
            self.con.execute_action_query(
                "UPDATE Screens SET screen_number = %s, seat_capacity = %s WHERE screen_id = %s;",
                (new_screen_number, new_seat_capacity, screen_id)
            )
            print(f"Screen with ID {screen_id} updated to screen number {new_screen_number} and capacity {new_seat_capacity}.")
        except Exception as e:
            print(f"Failed to update screen with ID {screen_id}:", e)

    def delete_screen(self, screen_id):
        try:
            # Screenings에서 해당 screen_id의 모든 screening_id 찾기
            results, columns = self.con.execute_query(
                "SELECT screening_id FROM Screenings WHERE screen_id = %s;", (screen_id,)
            )
            screenings = results

            # 해당 screening_id에 대한 Reservations 및 Seats 정보 삭제
            for screening in screenings:
                self.con.execute_action_query(
                    "DELETE FROM Reservations WHERE screening_id = %s;", (screening[0],)
                )
                self.con.execute_action_query(
                    "DELETE FROM Seats WHERE screen_id = %s AND screening_id = %s;", (screen_id, screening[0],)
                )
                self.con.execute_action_query(
                    "DELETE FROM Screenings WHERE screen_id = %s AND screening_id = %s;", (screen_id, screening[0],)
                )

            # Screens 테이블에서 해당 screen_id 삭제
            self.con.execute_action_query(
                "DELETE FROM Screens WHERE screen_id = %s;", (screen_id,)
            )
            print(f"Screen with ID {screen_id} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete screen with ID {screen_id}:", e)

    def close(self):
        self.con.close()