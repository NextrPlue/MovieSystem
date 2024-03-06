from database.databaseManager import DatabaseManager

class BookingInquirySystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def close(self):
        self.con.close()

    def get_reservations_by_user(self, user_id):
        query = """
        SELECT 
            r.reservation_id, 
            r.screening_id, 
            r.seat_id, 
            r.reservation_time, 
            r.payment_status,
            s.screen_id,
            s.screening_start_time,
            s.screening_end_time,
            ss.screen_number,
            m.movie_id,
            m.title,
            st.seat_number,
            rt.rating
        FROM Reservations r
        LEFT JOIN Screenings s ON r.screening_id = s.screening_id
        LEFT JOIN Screens ss ON s.screen_id = ss.screen_number
        LEFT JOIN Movies m ON s.movie_id = m.movie_id
        LEFT JOIN Seats st ON r.seat_id = st.seat_id
        LEFT JOIN Ratings rt ON r.user_id = rt.user_id AND m.movie_id = rt.movie_id
        WHERE r.user_id = %s;
        """
        try:
            results, columns = self.con.execute_query(query, (user_id,))
            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("Error fetching reservations:", e)
            return []

    def update_movie_rating(self, movie_id):
        # 특정 movie_id에 대한 평균 평점 계산
        avg_rating_query = """
        SELECT AVG(rating) as avg_rating
        FROM Ratings
        WHERE movie_id = %s
        GROUP BY movie_id;
        """

        try:
            avg_ratings, _ = self.con.execute_query(avg_rating_query, (movie_id,))

            # avg_ratings가 비어 있지 않은 경우에만 평균 평점을 Movies 테이블에 업데이트
            if avg_ratings:
                avg_rating = avg_ratings[0][0]  # 첫 번째 행의 첫 번째 열 (평균 평점)
                update_query = """
                UPDATE Movies
                SET rating = %s
                WHERE movie_id = %s;
                """
                self.con.execute_action_query(update_query, (avg_rating, movie_id))
                print(f"Rating for movie ID {movie_id} updated successfully.")
            else:
                print(f"No ratings found for movie ID {movie_id}.")
        except Exception as e:
            print(f"Error in updating rating for movie ID {movie_id}:", e)

    def add_movie_rating(self, user_id, movie_id, rating):
        # 평점이 이미 존재하는지 확인
        check_query = """
        SELECT rating_id 
        FROM Ratings 
        WHERE user_id = %s AND movie_id = %s;
        """
        try:
            results, _ = self.con.execute_query(check_query, (user_id, movie_id))
            if results:
                # 평점이 존재하면 업데이트
                update_query = """
                UPDATE Ratings 
                SET rating = %s, rating_time = CURRENT_TIMESTAMP 
                WHERE user_id = %s AND movie_id = %s;
                """
                self.con.execute_action_query(update_query, (rating, user_id, movie_id))
                print("Rating updated successfully.")
            else:
                # 평점이 존재하지 않으면 추가
                insert_query = """
                INSERT INTO Ratings (user_id, movie_id, rating) 
                VALUES (%s, %s, %s);
                """
                self.con.execute_action_query(insert_query, (user_id, movie_id, rating))
                print("Rating added successfully.")
            self.update_movie_rating(movie_id)
        except Exception as e:
            print("Error in adding/updating rating:", e)