import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from systems.movieBookingSystem import MovieBookingSystem

class MovieBookingScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.system = MovieBookingSystem()

        self.root.title("Movie Booking Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_movie_booking)

        self.create_widgets()
        self.seat_vars = {}  # 좌석 상태를 저장하는 딕셔너리

    def create_widgets(self):
        self.titlebox_frame = tk.Frame(self.root)
        self.combobox_frame = tk.Frame(self.root)
        self.checkbox_frame = tk.Frame(self.root)
        self.titlebox_frame.pack()
        self.combobox_frame.pack()
        self.checkbox_frame.pack()
        
        self.title = tk.Label(self.titlebox_frame, text="MOVIE BOOKING", justify=tk.CENTER)
        self.movie_combobox = ttk.Combobox(self.combobox_frame, state="readonly")
        self.time_combobox = ttk.Combobox(self.combobox_frame, state="readonly")
        self.screen_combobox = ttk.Combobox(self.combobox_frame, state="readonly")

        self.movie_combobox.bind("<<ComboboxSelected>>", self.on_movie_selected)
        self.time_combobox.bind("<<ComboboxSelected>>", self.on_time_selected)
        self.screen_combobox.bind("<<ComboboxSelected>>", self.on_screen_selected)

        # 콤보박스 위치 설정
        self.title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.movie_combobox.grid(row=0, column=0)
        self.time_combobox.grid(row=0, column=1)
        self.screen_combobox.grid(row=0, column=2)

        # 콤보박스에 데이터 채우기
        self.load_movies()

    def load_movies(self):
        movies = self.system.get_movies()
        # movie_id와 title을 매핑하는 딕셔너리 생성
        self.movie_id_title_map = {title: movie_id for title, movie_id in movies}
        # 콤보박스에 영화 제목을 채움
        self.movie_combobox['values'] = [title for title, movie_id in movies]
        self.movie_combobox.set('영화 선택')

    def on_movie_selected(self, event):
        movie_title = self.movie_combobox.get()
        movie_id = self.movie_id_title_map[movie_title]

        
        times = self.system.get_times(movie_id)
        self.time_combobox['values'] = [time[0] for time in times]
        self.time_combobox.set('시간 선택')
        self.screen_combobox['values'] = []
        self.screen_combobox.set('')

    def on_time_selected(self, event):
        movie_title = self.movie_combobox.get()
        movie_id = self.movie_id_title_map[movie_title]
        start_time = self.time_combobox.get()

        screens = self.system.get_screenings(movie_id, start_time)
        self.screen_combobox['values'] = [screen[0] for screen in screens]
        self.screen_combobox.set('상영관 선택')

    def on_screen_selected(self, event):
        screen_id = self.screen_combobox.get()
        movie_title = self.movie_combobox.get()
        movie_id = self.movie_id_title_map[movie_title]
        start_time = self.time_combobox.get()

        # 기존에 생성된 체크박스를 삭제
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        # Screenings 테이블에서 screening_id 조회
        screening_id_result = self.system.get_screening_id(movie_id, start_time, screen_id)
        
        if screening_id_result:
            self.screening_id = screening_id_result[0]

            # Seats 테이블에서 좌석 조회
            seats = self.system.get_seats(screen_id, self.screening_id)
            self.seat_id_number_map = {seat_number: seat_id for seat_id, seat_number, _ in seats}
            # 체크박스 생성
            for i, (seat_id, seat_number, is_available) in enumerate(seats):
                row = i // 10
                column = i % 10
                seat_var = tk.BooleanVar()
                chk = tk.Checkbutton(self.checkbox_frame, text=seat_number, variable=seat_var, state="normal" if is_available else "disabled")
                chk.grid(row=row, column=column)
                self.seat_vars[seat_number] = seat_var  # 좌석 번호와 변수 연결
            
            if seats:
                self.button = tk.Button(self.checkbox_frame, text="예약하기", command=self.book_selected_seats)
                self.button.grid()
        else:
            print("No matching screening found.")

    def get_selected_seats(self):
        # 선택된 좌석들의 번호를 반환
        seats = [self.seat_id_number_map[seat] for seat, var in self.seat_vars.items() if var.get()]
        return seats
    
    def book_selected_seats(self):
        seats = self.get_selected_seats()
        if seats:
            try:
                for seat_id in seats:
                    self.system.book_movie(self.user[0], self.screening_id, seat_id)
                self.system.update_booking_rate()
                messagebox.showinfo("Movie Booking Attempt", f"선택하신 좌석의 예약이 정상적으로 처리되었습니다.")
            except Exception as e:
                messagebox.showinfo("Movie Booking Attempt", f"예약하는 과정에서 오류가 발생하였습니다.\n{e}")

    def end_movie_booking(self):
        self.system.close()
        self.root.destroy()