import tkinter as tk
from systems.movieRecommenderSystem import MovieRecommenderSystem

class MovieRecommenderScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.system = MovieRecommenderSystem()

        self.root.title("Movie Recommender Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_movie_recommend)        

        # 검색 결과와 페이지 관련 변수
        self.recommended_movies = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_search()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="MOVIE RECOMMEND", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")

        self.result_display = tk.Text(self.root, height=10, width=50)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.result_display.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.btn_prev.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.btn_next.grid(row=3, column=2, padx=10, pady=10, sticky=tk.E)
        
    def perform_search(self):
        # 예시 검색 결과
        # 실제로는 여기서 검색 쿼리 결과를 받아옵니다.
        self.recommended_movies, self.ad_movie = self.system.recommend_movies(self.user[0])
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.recommended_movies):
            movie = self.recommended_movies[self.current_page]
            display_text = f"Title: {movie['title']}\nGenre: {movie['genre']}\nRating: {float(movie['rating'])}\nBooking-Rating: {movie['booking_rate']}\nDescription: {movie['description']}"
            if self.ad_movie and self.current_page == 0:
                display_text = f"[Advertisement]\n\n" + display_text
            self.result_display.insert(tk.END, display_text)    
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.recommended_movies) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def end_movie_recommend(self):
        self.system.close()
        self.root.destroy()