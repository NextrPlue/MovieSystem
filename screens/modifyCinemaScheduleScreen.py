import tkinter as tk
from tkinter import messagebox
from systems.cinemaScheduleSystem import CinemaScheduleSystem

class ModifyCinemaScheduleScreen:
    def __init__(self, root):
        self.root = root
        self.system = CinemaScheduleSystem()

        self.current_screening_id = ""

        self.root.title("Screening Management Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_modify_screening)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_get_screening()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="SCREENING MANAGEMENT", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_delete = tk.Button(self.root, text="삭제하기", command=self.delete_screening)

        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")
    
        self.result_display = tk.Text(self.root, height=9, width=50)

        label_title.grid(row=0, column=1, columnspan=2, pady=(5, 0))
        self.result_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.btn_delete.grid(row=2, column=3, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)
        self.btn_next.grid(row=4, column=3, padx=10, pady=10, sticky=tk.E)

    def perform_get_screening(self):
        self. search_results = self.system.get_screenings_info()
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            screening = self.search_results[self.current_page]
            display_text = (
                f"Screening ID: {screening['screening_id']}\n\n"
                f"Screen ID: {screening['screen_id']}\n\n"
                f"Movie Title: {screening['title']}\n\n"
                f"Start Time: {screening['screening_start_time']}\n\n"
                f"End Time: {screening['screening_end_time']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_screening_id = screening['screening_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def delete_screening(self):
        try:
            if (self.current_screening_id):
                self.system.remove_screening(self.current_screening_id)
                messagebox.showinfo("Screen Modify Attempt", f"성공적으로 상영 정보가 삭제되었습니다.")
            else:
                messagebox.showinfo("Screen Modify Attempt", f"상영 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Screen Modify Attempt", f"상영 정보 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_screening()

    def end_modify_screening(self):
        self.system.close()
        self.root.destroy()