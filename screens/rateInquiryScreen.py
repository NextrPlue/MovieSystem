import tkinter as tk
from tkinter import ttk
from systems.searchMovieSystem import SearchMovieSystem

class RateInquiryScreen:
    def __init__(self, root):
        self.root = root
        self.system = SearchMovieSystem()

        self.root.title("Rate Inquiry Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_search_movie)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()


    def create_widgets(self):
        label_title = tk.Label(self.root, text="RATE INQUIRY", justify=tk.CENTER)

        self.search_category = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.search_category, 
                                          values=["제목", "감독", "장르"])
        self.category_menu.current(0)  # 기본값 설정

        self.search_entry = tk.Entry(self.root)

        self.genre_category = tk.StringVar()
        self.genre_menu = ttk.Combobox(self.root, textvariable=self.genre_category,
                                       values=self.system.get_genres())
        self.genre_menu.current(0)  # 기본값 설정

        search_button = tk.Button(self.root, text="검색", command=self.perform_search)
        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")

        self.result_display = tk.Text(self.root, height=10, width=50)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.category_menu.grid(row=1, column=0, padx=10, pady=10)
        self.category_menu.bind("<<ComboboxSelected>>", self.update_search_field)
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)
        # self.genre_menu.grid(row=1, column=1, padx=10, pady=10)  # 초기에는 숨김
        search_button.grid(row=1, column=2, padx=10, pady=10)
        self.result_display.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.btn_prev.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.btn_next.grid(row=3, column=2, padx=10, pady=10, sticky=tk.E)

        self.perform_search()

    def update_search_field(self, event=None):
        # 선택된 카테고리에 따라 검색 필드를 전환
        if self.search_category.get() == "장르":
            self.search_entry.grid_remove()
            self.genre_menu.grid(row=1, column=1, padx=10, pady=10)
        else:
            self.genre_menu.grid_remove()
            self.search_entry.grid(row=1, column=1, padx=10, pady=10)

    def perform_search(self):
        # 예시 검색 결과
        # 실제로는 여기서 검색 쿼리 결과를 받아옵니다.
        if self.search_category.get() == "제목":
            self.search_results = self.system.search_movie("title", self.search_entry.get())
        if self.search_category.get() == "감독":
            self.search_results = self.system.search_movie("director", self.search_entry.get())
        if self.search_category.get() == "장르":
            self.search_results = self.system.search_movie("genre", self.genre_category.get())

        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            movie = self.search_results[self.current_page]
            display_text = f"Title: {movie['title']}\nGenre: {movie['genre']}\nRating: {float(movie['rating'])}\nBooking-Rating: {movie['booking_rate']}\nIs Showing: {movie['is_showing']}"
            self.result_display.insert(tk.END, display_text)    
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def end_search_movie(self):
        self.system.close()
        self.root.destroy()