import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from systems.cinemaScheduleSystem import CinemaScheduleSystem
import datetime

class AddCinemaScheduleScreen:
    def __init__(self, root):
        self.root = root
        self.system = CinemaScheduleSystem()

        self.root.title("Screening Add Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_add_screening)

        self.create_widgets()


    def create_widgets(self):
        self.titlebox_frame = tk.Frame(self.root)
        self.combobox_frame = tk.Frame(self.root)
        self.entrybox_frame = tk.Frame(self.root)
        self.cal = Calendar(self.root, selectmode='day')
        self.titlebox_frame.pack()
        self.combobox_frame.pack()
        self.cal.pack(padx=10, pady=10)
        self.entrybox_frame.pack()

        validate_command = (self.root.register(self.only_numbers), '%S')
        
        label_title = tk.Label(self.titlebox_frame, text="SCREEN ADD", justify=tk.CENTER)
        label_start_time = tk.Label(self.entrybox_frame, text="Start Time:")
        label_start_hour = tk.Label(self.entrybox_frame, text="시")
        label_start_minute = tk.Label(self.entrybox_frame, text="분")

        self.start_hour_entry = tk.Entry(self.entrybox_frame, validate='key', validatecommand=validate_command)
        self.start_minute_entry = tk.Entry(self.entrybox_frame, validate='key', validatecommand=validate_command)

        add_button = tk.Button(self.entrybox_frame, text="추가", command=self.attempt_add_screening)

        self.movie_combobox = ttk.Combobox(self.combobox_frame, state="readonly")
        self.screen_combobox = ttk.Combobox(self.combobox_frame, state="readonly")

        self.movie_combobox.bind("<<ComboboxSelected>>", self.on_movie_selected)
        self.screen_combobox.bind("<<ComboboxSelected>>", self.on_screen_selected)

        # 콤보박스 위치 설정
        self.movie_combobox.grid(row=0, column=0)
        self.screen_combobox.grid(row=0, column=1)

        label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0))
        label_start_time.grid(row=1, column=0, sticky=tk.E)
        self.start_hour_entry.grid(row=1, column=1, sticky=tk.W)
        label_start_hour.grid(row=1, column=2, sticky=tk.E)
        self.start_minute_entry.grid(row=1, column=3, sticky=tk.W)
        label_start_minute.grid(row=1, column=4, sticky=tk.E)
        add_button.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

        self.load_movies()
        self.load_screens()
        
    def attempt_add_screening(self):
        try:          
            start_datetime, end_datetime = self.get_schedule()
            self.system.add_screening(self.screen_id, self.movie_id, start_datetime, end_datetime)
            messagebox.showinfo("Add Screen Attempt", 
                                (f"성공적으로 상영관을 추가하였습니다.\n"
                                f"Movie Title: {self.movie_title}\n"
                                f"Screen Number: {self.screen_number}\n"
                                f"Start Time: {start_datetime}\n"
                                f"End Time: {end_datetime}"))
        except AttributeError as e:
            messagebox.showinfo("Add Screen Attempt", f"상영관을 추가하는 과정에서 오류가 발생하였습니다.\n상영관 및 영화를 선택해주세요.")
        except Exception as e:
            messagebox.showinfo("Add Screen Attempt", f"상영관을 추가하는 과정에서 오류가 발생하였습니다.\n{e}")

    def load_movies(self):
        movies = self.system.get_movies_info()
        # movie_id와 title을 매핑하는 딕셔너리 생성
        self.movie_id_title_map = {movie['title']: (movie['movie_id'], movie['runtime']) for movie in movies}
        # 콤보박스에 영화 제목을 채움
        self.movie_combobox['values'] = [movie['title'] for movie in movies]
        self.movie_combobox.set('영화 선택')

    def load_screens(self):
        screens = self.system.get_screens_info()
        # movie_id와 title을 매핑하는 딕셔너리 생성
        self.screen_id_number_map = {screen['screen_number']: screen['screen_id'] for screen in screens}
        # 콤보박스에 영화 제목을 채움
        self.screen_combobox['values'] = [screen['screen_number'] for screen in screens]
        self.screen_combobox.set('상영관 선택')    

    def on_movie_selected(self, event):
        self.movie_title = self.movie_combobox.get()
        self.movie_id, self.movie_runtime = self.movie_id_title_map[self.movie_title]

    def on_screen_selected(self, event):
        self.screen_number = int(self.screen_combobox.get())
        self.screen_id = self.screen_id_number_map[self.screen_number]

    def get_schedule(self):
        date = self.cal.get_date()
        runtime = self.movie_runtime
        try:
            start_hour = int(self.start_hour_entry.get())
            start_minute = int(self.start_minute_entry.get())           
        except Exception:
            raise ValueError("시작 시간 및 종료 시간을 입력해주세요.")

        # 시작 시간 계산
        start_datetime = datetime.datetime.strptime(f'{date} {start_hour}:{start_minute}', '%m/%d/%y %H:%M')
        
        # 종료 시간 계산: runtime을 분 단위로 더함
        end_datetime = start_datetime + datetime.timedelta(minutes=runtime)

        # datetime 객체를 문자열로 변환
        start_datetime_str = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')

        return start_datetime_str, end_datetime_str

    def only_numbers(self, char):
        return char.isdigit()

    def end_add_screening(self):
        self.system.close()
        self.root.destroy()