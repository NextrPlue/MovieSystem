import tkinter as tk
from .searchMovieScreen import SearchMovieScreen
from .movieRecommenderScreen import MovieRecommenderScreen
from .movieBookingScreen import MovieBookingScreen
from .bookingInquiryScreen import BookingInquiryScreen
from .screenAddScreen import ScreenAddScreen
from .screenModifyScreen import ScreenModifyScreen
from .addCinemaScheduleScreen import AddCinemaScheduleScreen
from .modifyCinemaScheduleScreen import ModifyCinemaScheduleScreen
from .userManagementScreen import UserManagementScreen
from .movieAddScreen import MovieAddScreen
from .movieModifyScreen import MovieModifyScreen
from .adManagementScreen import AdManagementScreen
from .rateInquiryScreen import RateInquiryScreen

class MainScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Main Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 홈 화면 레이아웃 구성
        if self.user[4] == 'customer':
            self.create_customer_widgets()
        elif self.user[4]== 'admin':
            self.create_admin_widgets()
        else:
            self.create_distributor_widgets()

    def open_new_window(self, window_class, *args, **kwargs):
        new_window = tk.Toplevel(self.root)
        window_app = window_class(new_window, *args, **kwargs)
        new_window.grab_set()

    def open_search_movie_screen(self):
        self.open_new_window(SearchMovieScreen)

    def open_movie_recommender_screen(self):
        self.open_new_window(MovieRecommenderScreen, self.user)

    def open_movie_booking_screen(self):
        self.open_new_window(MovieBookingScreen, self.user)

    def open_booking_inquiry_screen(self):
        self.open_new_window(BookingInquiryScreen, self.user)

    def open_screen_add_screen(self):
        self.open_new_window(ScreenAddScreen)

    def open_screen_modify_screen(self):
        self.open_new_window(ScreenModifyScreen)

    def open_add_cinema_schedule_screen(self):
        self.open_new_window(AddCinemaScheduleScreen)

    def open_modify_cinema_schedule_screen(self):
        self.open_new_window(ModifyCinemaScheduleScreen)

    def open_user_management_screen(self):
        self.open_new_window(UserManagementScreen)

    def open_movie_add_screen(self):
        self.open_new_window(MovieAddScreen)

    def open_movie_modify_screen(self):
        self.open_new_window(MovieModifyScreen)

    def open_ad_management_screen(self):
        self.open_new_window(AdManagementScreen, self.user)

    def open_rate_inquiry_screen(self):
        self.open_new_window(RateInquiryScreen)

    def close_screen(self):
        self.root.destroy()  # 창 닫기

    def create_customer_widgets(self):
        label_title = tk.Label(self.root, text="PNU MOVIE", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text=f"{self.user[1]}님 환영합니다!\n카테고리를 선택하여 주십시오.", justify=tk.LEFT)
        
        button1 = tk.Button(self.root, text="영화 검색", command=self.open_search_movie_screen)
        button2 = tk.Button(self.root, text="추천 영화", command=self.open_movie_recommender_screen)
        button3 = tk.Button(self.root, text="영화 예매", command=self.open_movie_booking_screen)
        button4 = tk.Button(self.root, text="예매 조회 및 평점 작성", command=self.open_booking_inquiry_screen)
        button5 = tk.Button(self.root, text="프로그램 종료", command=self.close_screen)

        # grid를 사용한 위젯 배치
        label_title.pack(pady=(5, 0))
        label_welcome.pack(pady=(5, 5))
        button1.pack(fill=tk.X, padx=10, pady=5)
        button2.pack(fill=tk.X, padx=10, pady=5)
        button3.pack(fill=tk.X, padx=10, pady=5)
        button4.pack(fill=tk.X, padx=10, pady=5)
        button5.pack(fill=tk.X, padx=10, pady=5)

    def create_admin_widgets(self):
        label_title = tk.Label(self.root, text="PNU MOVIE", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text=f"{self.user[1]}님 환영합니다!\n카테고리를 선택하여 주십시오.", justify=tk.LEFT)
        
        button1 = tk.Button(self.root, text="상영관 정보 등록", command=self.open_screen_add_screen)
        button2 = tk.Button(self.root, text="상영관 정보 조회 및 수정", command=self.open_screen_modify_screen)
        button3 = tk.Button(self.root, text="상영 시간표 등록", command=self.open_add_cinema_schedule_screen)
        button4 = tk.Button(self.root, text="상영 시간표 조회 및 수정", command=self.open_modify_cinema_schedule_screen)
        button5 = tk.Button(self.root, text="사용자 관리", command=self.open_user_management_screen)
        button6 = tk.Button(self.root, text="프로그램 종료", command=self.close_screen)

        # grid를 사용한 위젯 배치
        label_title.pack(pady=(5, 0))
        label_welcome.pack(pady=(5, 5))
        button1.pack(fill=tk.X, padx=10, pady=5)
        button2.pack(fill=tk.X, padx=10, pady=5)
        button3.pack(fill=tk.X, padx=10, pady=5)
        button4.pack(fill=tk.X, padx=10, pady=5)
        button5.pack(fill=tk.X, padx=10, pady=5)
        button6.pack(fill=tk.X, padx=10, pady=5)

    def create_distributor_widgets(self):
        label_title = tk.Label(self.root, text="PNU MOVIE", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text=f"{self.user[1]}님 환영합니다!\n카테고리를 선택하여 주십시오.", justify=tk.LEFT)
        
        button1 = tk.Button(self.root, text="영화 등록", command=self.open_movie_add_screen)
        button2 = tk.Button(self.root, text="영화 조회 및 수정", command=self.open_movie_modify_screen)
        button3 = tk.Button(self.root, text="광고 등록 및 삭제", command=self.open_ad_management_screen)
        button4 = tk.Button(self.root, text="예매율 조회", command=self.open_rate_inquiry_screen)
        button5 = tk.Button(self.root, text="프로그램 종료", command=self.close_screen)

        # grid를 사용한 위젯 배치
        label_title.pack(pady=(5, 0))
        label_welcome.pack(pady=(5, 5))
        button1.pack(fill=tk.X, padx=10, pady=5)
        button2.pack(fill=tk.X, padx=10, pady=5)
        button3.pack(fill=tk.X, padx=10, pady=5)
        button4.pack(fill=tk.X, padx=10, pady=5)
        button5.pack(fill=tk.X, padx=10, pady=5)