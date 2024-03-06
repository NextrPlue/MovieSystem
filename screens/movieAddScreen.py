import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import Calendar
from systems.movieManagementSystem import MovieManagementSystem

class MovieAddScreen:
    def __init__(self, root):
        self.root = root
        self.system = MovieManagementSystem()

        self.root.title("Movie Add Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_add_movie)

        self.create_widgets()


    def create_widgets(self):
        validate_command = (self.root.register(self.only_numbers), '%S')
        
        label_title = tk.Label(self.root, text="Movie ADD", justify=tk.CENTER)
        label_movie_title = tk.Label(self.root, text="Movie Title:")
        label_director = tk.Label(self.root, text="Director:")
        label_runtime = tk.Label(self.root, text="Runtime:")
        label_genre = tk.Label(self.root, text="Genre:")
        label_release_date = tk.Label(self.root, text="Release Date:")
        label_description = tk.Label(self.root, text="Description:")
        label_price = tk.Label(self.root, text="Price:")

        self.movie_title_entry = tk.Entry(self.root)
        self.director_entry = tk.Entry(self.root)
        self.runtime_entry = tk.Entry(self.root, validate='key', validatecommand=validate_command)
        self.genre_entry = tk.Entry(self.root)
        self.release_date_entry = tk.Entry(self.root)
        self.description_entry = tk.Entry(self.root)
        self.price_entry = tk.Entry(self.root, validate='key', validatecommand=validate_command)

        release_date_button = tk.Button(self.root, text="Select Date", command=self.open_calendar)
        add_button = tk.Button(self.root, text="추가", command=self.attempt_add_movie)

        label_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(5, 0))
        label_movie_title.grid(row=1, column=0, sticky=tk.E)
        self.movie_title_entry.grid(row=1, column=1, sticky=tk.W)
        label_director.grid(row=2, column=0, sticky=tk.E)
        self.director_entry.grid(row=2, column=1, sticky=tk.W)
        label_runtime.grid(row=3, column=0, sticky=tk.E)
        self.runtime_entry.grid(row=3, column=1, sticky=tk.W)
        label_genre.grid(row=4, column=0, sticky=tk.E)
        self.genre_entry.grid(row=4, column=1, sticky=tk.W)
        label_release_date.grid(row=5, column=0, sticky=tk.E)
        self.release_date_entry.grid(row=5, column=1, sticky=tk.W)
        release_date_button.grid(row=5, column=2, padx=10)
        label_description.grid(row=6, column=0, sticky=tk.E)
        self.description_entry.grid(row=6, column=1, sticky=tk.W)
        label_price.grid(row=7, column=0, sticky=tk.E)
        self.price_entry.grid(row=7, column=1, sticky=tk.W)
        add_button.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

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

    def attempt_add_movie(self):
        movie_title = self.movie_title_entry.get()
        director = self.director_entry.get()
        runtime = self.runtime_entry.get()
        genre = self.genre_entry.get()
        release_date = self.release_date_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()

        try:
            self.system.add_movie(movie_title, director, runtime, genre, release_date, description, price)
            messagebox.showinfo("Add Movie Attempt", f"성공적으로 영화를 추가하였습니다.")
        except Exception as e:
            messagebox.showinfo("Add Movie Attempt", f"영화를 추가하는 과정에서 오류가 발생하였습니다.\n{e}")

    def only_numbers(self, char):
        return char.isdigit()

    def end_add_movie(self):
        self.system.close()
        self.root.destroy()