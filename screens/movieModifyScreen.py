import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import Calendar
from systems.movieManagementSystem import MovieManagementSystem

class MovieModifyScreen:
    def __init__(self, root):
        self.root = root
        self.system = MovieManagementSystem()

        self.current_movie_id = ""

        self.root.title("Movie Management Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_modify_movie)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_get_movie()

    def create_widgets(self):
        is_only_number = (self.root.register(self.only_numbers), '%S')
        is_decimal = (self.root.register(self.is_decimal), '%S')
        
        label_title = tk.Label(self.root, text="MOVIE MANAGEMENT", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_delete = tk.Button(self.root, text="삭제하기", command=self.delete_movie)
        self.btn_modify = tk.Button(self.root, text="수정하기", command=self.update_movie)
        release_date_button = tk.Button(self.root, text="Select Date", command=self.open_calendar)

        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")
        label_movie_title = tk.Label(self.root, text="Movie Title:")
        label_director = tk.Label(self.root, text="Director:")
        label_runtime = tk.Label(self.root, text="Runtime:")
        label_genre = tk.Label(self.root, text="Genre:")
        label_release_date = tk.Label(self.root, text="Release Date:")
        label_description = tk.Label(self.root, text="Description:")
        label_price = tk.Label(self.root, text="Price:")

        self.movie_title_entry = tk.Entry(self.root)
        self.director_entry = tk.Entry(self.root)
        self.runtime_entry = tk.Entry(self.root, validate='key', validatecommand=is_only_number)
        self.genre_entry = tk.Entry(self.root)
        self.release_date_entry = tk.Entry(self.root)
        self.description_entry = tk.Entry(self.root)
        self.price_entry = tk.Entry(self.root, validate='key', validatecommand=is_decimal)
        self.result_display = tk.Text(self.root, height=18, width=40)

        label_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(5, 0))
        self.result_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        label_movie_title.grid(row=2, column=0, sticky=tk.E)
        self.movie_title_entry.grid(row=2, column=1, sticky=tk.W)
        label_director.grid(row=3, column=0, sticky=tk.E)
        self.director_entry.grid(row=3, column=1, sticky=tk.W)
        label_runtime.grid(row=4, column=0, sticky=tk.E)
        self.runtime_entry.grid(row=4, column=1, sticky=tk.W)
        label_genre.grid(row=5, column=0, sticky=tk.E)
        self.genre_entry.grid(row=5, column=1, sticky=tk.W)
        label_release_date.grid(row=6, column=0, sticky=tk.E)
        self.release_date_entry.grid(row=6, column=1, sticky=tk.W)
        release_date_button.grid(row=6, column=2, padx=10)
        label_description.grid(row=7, column=0, sticky=tk.E)
        self.description_entry.grid(row=7, column=1, sticky=tk.W)
        label_price.grid(row=8, column=0, sticky=tk.E)
        self.price_entry.grid(row=8, column=1, sticky=tk.W)        
        self.btn_modify.grid(row=9, column=1, sticky=tk.E)
        self.btn_delete.grid(row=9, column=2, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=10, column=1, padx=10, pady=10, sticky=tk.E)
        self.btn_next.grid(row=10, column=2, padx=10, pady=10, sticky=tk.E)

    def open_calendar(self):
        def set_date():
            self.release_date_entry.delete(0, tk.END)
            self.release_date_entry.insert(0, cal.selection_get().strftime("%Y-%m-%d"))
            top.destroy()

        top = Toplevel(self.root)
        top.title("Select Date")
        cal = Calendar(top, selectmode='day')
        cal.pack(pady=10)
        ok_button = tk.Button(top, text="OK", command=set_date)
        ok_button.pack()

    def perform_get_movie(self):
        self. search_results = self.system.get_all_movies()
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            movie = self.search_results[self.current_page]
            self.movie_title_entry.delete(0, tk.END)
            self.director_entry.delete(0, tk.END)
            self.runtime_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.release_date_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.movie_title_entry.insert(0, movie['title'])
            self.director_entry.insert(0, movie['director'])
            self.runtime_entry.insert(0, movie['runtime'])
            self.genre_entry.insert(0, movie['genre'])
            self.release_date_entry.insert(0, movie['release_date'])
            self.description_entry.insert(0, movie['description'])
            self.price_entry.insert(0, movie['price'])
            display_text = (
                f"Movie ID: {movie['movie_id']}\n\n"
                f"Title: {movie['title']}\n\n"
                f"Director: {movie['director']}\n\n"
                f"Runtime: {movie['runtime']}\n\n"
                f"Genre: {movie['genre']}\n\n"
                f"Release Date: {movie['release_date']}\n\n"
                f"Description: {movie['description']}\n\n"
                f"Price: {movie['price']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_movie_id = movie['movie_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def delete_movie(self):
        try:
            if (self.current_movie_id):
                self.system.delete_movie(self.current_movie_id)
                messagebox.showinfo("Movie Modify Attempt", f"성공적으로 영화 정보가 삭제되었습니다.")
            else:
                messagebox.showinfo("Movie Modify Attempt", f"영화 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Movie Modify Attempt", f"영화 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_movie()

    def update_movie(self):
        title = self.movie_title_entry.get()
        director = self.director_entry.get()
        runtime = self.runtime_entry.get()
        genre = self.genre_entry.get()
        release_date = self.release_date_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        try:
            self.system.update_movie(self.current_movie_id, title, director, runtime, genre, release_date, description, price)
            messagebox.showinfo("Movie Modify Attempt", f"성공적으로 영화 정보가 수정되었습니다.")
        except Exception as e:
            messagebox.showinfo("Movie Modify Attempt", f"영화 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_movie()

    def only_numbers(self, char):
        return char.isdigit()

    def is_decimal(self, char):
        if char == "" or char == ".":
            return True
        try:
            float(char)
            return len(char.split('.')[1]) <= 2 if '.' in char else True
        except ValueError:
            return False

    def end_modify_movie(self):
        self.system.close()
        self.root.destroy()