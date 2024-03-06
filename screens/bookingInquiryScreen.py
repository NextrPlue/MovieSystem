import tkinter as tk
from tkinter import messagebox
from systems.bookingInquirySystem import BookingInquirySystem
from systems.movieBookingSystem import MovieBookingSystem

class BookingInquiryScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.system = BookingInquirySystem()

        self.current_screening_id = ""
        self.current_seat_id = ""

        self.root.title("Booking Inquiry Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_booking_inquiry)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_search()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="BOOKING INQUIRY", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_cancel_booking = tk.Button(self.root, text="예매 취소", command=self.cancel_booking)
        self.btn_rating = tk.Button(self.root, text="평점 등록", command=self.add_rating)

        validate_command = (self.root.register(self.validate_rating), '%P')
        self.rating_entry = tk.Entry(self.root, validate='key', validatecommand=validate_command)

        guide_label = tk.Label(self.root, text="평점 입력 (0.0 ~ 9.9):")
        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")

        self.result_display = tk.Text(self.root, height=11, width=50)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        guide_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.rating_entry.grid(row=1, column=1, sticky=tk.W)
        self.btn_rating.grid(row=1, column=2, pady=10, sticky=tk.W)
        self.result_display.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.btn_cancel_booking.grid(row=3, column=2, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.btn_next.grid(row=4, column=2, padx=10, pady=10, sticky=tk.E)

    def perform_search(self):
        self. search_results = self.system.get_reservations_by_user(self.user[0])
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            movie = self.search_results[self.current_page]
            display_text = (
                f"Title: {movie['title']}\n\n"
                f"Start time: {movie['screening_start_time']}\n\n"
                f"End time: {movie['screening_end_time']}\n\n"
                f"Screen Number: {movie['screen_number']}\n\n"
                f"Seat Number: {movie['seat_number']}\n\n"
                f"My Rating: {movie['rating']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_movie_id = movie['movie_id']
            self.current_screening_id = movie['screening_id']
            self.current_seat_id = movie['seat_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def add_rating(self):
        rating = self.rating_entry.get()
        try:
            if rating:
                self.system.add_movie_rating(self.user[0], self.current_movie_id, rating)
                messagebox.showinfo("Add Rating Attempt", f"성공적으로 평점을 추가하였습니다.")
                self.perform_search()
            else:
                messagebox.showinfo("Add Rating Attempt", f"평점을 입력해주세요.")
        except Exception as e:
            messagebox.showinfo("Add Rating Attempt", f"평점을 추가하는 과정에서 오류가 발생하였습니다.\n{e}")

    def cancel_booking(self):
        cancel_system = MovieBookingSystem()
        try:
            if (self.user[0] and self.current_screening_id and self.current_seat_id):
                cancel_system.cancel_movie_booking(self.user[0], self.current_screening_id, self.current_seat_id)
                messagebox.showinfo("Booking Cancel Attempt", f"성공적으로 예매가 취소되었습니다.")
            else:
                messagebox.showinfo("Booking Cancel Attempt", f"예매 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Booking Cancel Attempt", f"예매 취소 과정에서 오류가 발생하였습니다.\n{e}")
        cancel_system.close()
        self.perform_search()

    def validate_rating(self, rating):
        # 평점이 0.0에서 10.0 사이이며 소수점 첫 번째 자리까지만 허용
        try:
            if rating in ["", "."]:  # 빈 문자열과 단독 소수점은 허용
                return True
            rating_float = float(rating)
            return (0.0 <= rating_float < 10.0) and (len(rating.split('.')) == 1 or len(rating.split('.')[1]) <= 1)
        except ValueError:  # 숫자로 변환할 수 없는 입력은 거부
            return False

    def end_booking_inquiry(self):
        self.system.close()
        self.root.destroy()