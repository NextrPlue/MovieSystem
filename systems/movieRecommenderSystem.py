import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from database.databaseManager import DatabaseManager

class MovieRecommenderSystem:
    def __init__(self):
        self.con = DatabaseManager()
        self.con.connect()

    def fetch_user_ratings(self):
        query = """
            SELECT r.user_id, r.movie_id, r.rating 
            FROM Ratings r
            INNER JOIN Screenings s ON r.movie_id = s.movie_id
            GROUP BY r.user_id, r.movie_id, r.rating;
            """
        results, columns = self.con.execute_query(query)
        return pd.DataFrame(results, columns=columns)
    
    def fetch_user_reservations(self):
        query = """
            SELECT r.user_id, s.movie_id
            FROM Reservations r
            INNER JOIN Screenings s ON r.screening_id = s.screening_id
            GROUP BY r.user_id, s.movie_id;
            """
        results, columns = self.con.execute_query(query)
        return pd.DataFrame(results, columns=columns)

    def calculate_cosine_similarity(self, reservations_df):
        # 사용자별 영화 예매 정보를 피벗 테이블로 변환
        user_movie_reservations = pd.pivot_table(
            data=reservations_df, 
            values='movie_id', 
            index='user_id', 
            columns='movie_id', 
            aggfunc=lambda x: len(x), 
            fill_value=0
        )

        # 피벗 테이블에 적어도 하나 이상의 열이 있는지 확인
        if user_movie_reservations.shape[1] == 0:
            raise ValueError("No features (movies) found for cosine similarity calculation")

        similarity_matrix = cosine_similarity(user_movie_reservations)
        return similarity_matrix, user_movie_reservations

    def find_similar_users(self, user_id, similarity_matrix, user_movie_ratings):
        user_idx = {id: index for index, id in enumerate(user_movie_ratings.index)}
        user_similarities = similarity_matrix[user_idx[user_id]]
        similar_user_idx = np.argsort(-user_similarities)[1:6]  # Top 5 similar users excluding themselves
        similar_users = user_movie_ratings.index[similar_user_idx].tolist()
        return similar_users

    def get_movie_details(self, movie_ids):
        movie_ids_tuple = tuple(movie_ids)
        query = f"""
            SELECT * FROM Movies WHERE movie_id IN %s;
            """
        results, columns = self.con.execute_query(query, (movie_ids_tuple,))
        movies = [dict(zip(columns, row)) for row in results]
        
        # 추천 순서에 따라 영화를 정렬
        movie_id_to_info = {movie['movie_id']: movie for movie in movies}
        ordered_movies = [movie_id_to_info[movie_id] for movie_id in movie_ids if movie_id in movie_id_to_info]
        
        return ordered_movies

    def recommend_movies(self, user_id):
        # 평점 데이터와 예매 데이터를 가져옴
        ratings_df = self.fetch_user_ratings()
        reservations_df = self.fetch_user_reservations()

        # 평점 데이터와 예매 데이터를 결합
        ratings_df['interaction'] = 1
        combined_df = pd.concat([ratings_df[['user_id', 'movie_id', 'interaction']], reservations_df[['user_id', 'movie_id']]], ignore_index=True)
        combined_df['interaction'] = combined_df.groupby(['user_id', 'movie_id'])['interaction'].transform('count')

        try:
            # 코사인 유사도 계산
            similarity_matrix, user_movie_ratings = self.calculate_cosine_similarity(combined_df)
            
            # 사용자가 평점 또는 예매한 영화가 있는지 확인
            if user_id in user_movie_ratings.index:
                similar_users = self.find_similar_users(user_id, similarity_matrix, user_movie_ratings)
                # 추천 영화 선택
                recommended_movies_id = user_movie_ratings.loc[similar_users].sum().sort_values(ascending=False).head(5).index.tolist()
            else:
                raise ValueError
        except ValueError:
            # 코사인 유사도를 계산할 수 없는 경우 무작위로 5개의 영화 추천
            random_movies, _ = self.con.execute_query(
                "SELECT movie_id FROM Movies ORDER BY RANDOM() LIMIT 5;"
            )
            recommended_movies_id = [movie[0] for movie in random_movies] if random_movies else []

        # 추천 영화 목록을 가져옴
        recommended_movies = self.get_movie_details(recommended_movies_id)

        # Advertisements 테이블에서 무작위로 영화를 하나 선택
        ad_movie, _ = self.con.execute_query(
            "SELECT movie_id FROM Advertisements ORDER BY RANDOM() LIMIT 1;"
        )
        ad_movie_id = ad_movie[0][0] if ad_movie else None

        # 광고된 영화가 있으면 추천 목록의 가장 앞에 추가
        if ad_movie_id:
            ad_movie_detail = self.get_movie_details([ad_movie_id])[0]
            recommended_movies.insert(0, ad_movie_detail)

        return recommended_movies, ad_movie_id


    def close(self):
        self.con.close()