from database.databaseManager import DatabaseManager

class SearchMovieSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def search_movie(self, field, search_term):
        query = f"""
            SELECT DISTINCT m.*, 
                    CASE 
                        WHEN s.movie_id IS NOT NULL THEN TRUE 
                        ELSE FALSE 
                    END as is_showing
            FROM Movies m
            LEFT JOIN Screenings s ON m.movie_id = s.movie_id
            WHERE {field} ILIKE %s
            """
        search_term = f"%{search_term}%"  # 포함 검색을 위한 패턴

        results, columns = self.con.execute_query(query, (search_term,))
        return [dict(zip(columns, row)) for row in results]

    def get_genres(self):
        query = "SELECT DISTINCT genre FROM Movies ORDER BY genre ASC;"
        try:
            results, _ = self.con.execute_query(query)
            return [genre[0] for genre in results]  # 장르만 추출
        except Exception as e:
            print("Error fetching unique genres:", e)
            return []

    def close(self):
        self.con.close()
