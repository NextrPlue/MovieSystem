from database.databaseManager import DatabaseManager
from .movieBookingSystem import MovieBookingSystem

class UserManagementSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def get_all_users(self):
        query = "SELECT * FROM Users ORDER BY user_id ASC;"
        try:
            results, columns = self.con.execute_query(query)
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("Error fetching user data:", e)
            return []

    def delete_user(self, user_id):
        try:
            booking_system = MovieBookingSystem()

            # 해당 사용자의 모든 예약 찾기
            reservations, _ = self.con.execute_query(
                "SELECT screening_id, seat_id FROM Reservations WHERE user_id = %s;",
                (user_id,)
            )

            # 각 예약에 대해 예약 취소 수행
            for screening_id, seat_id in reservations:
                booking_system.cancel_movie_booking(user_id, screening_id, seat_id)

            # Ratings 테이블에서 해당 사용자의 평점 정보 삭제
            self.con.execute_action_query(
                "DELETE FROM Ratings WHERE user_id = %s;",
                (user_id,)
            )

            # Users 테이블에서 해당 사용자 삭제
            self.con.execute_action_query(
                "DELETE FROM Users WHERE user_id = %s;",
                (user_id,)
            )

            print(f"User with ID {user_id} and all related data deleted successfully.")
            booking_system.close()
        except Exception as e:
            print(f"Error in deleting user with ID {user_id}:", e)

    def update_user_role(self, user_id, new_role):
        if new_role not in ['customer', 'admin', 'distributor']:
            print("Invalid role. Role must be 'customer', 'admin', or 'distributor'.")
            return

        query = "UPDATE Users SET user_role = %s WHERE user_id = %s;"
        try:
            self.con.execute_action_query(query, (new_role, user_id))
            print(f"User role for user ID {user_id} updated to {new_role}.")
        except Exception as e:
            print("Error updating user role:", e)

    def close(self):
        self.con.close()