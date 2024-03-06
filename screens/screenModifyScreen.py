import tkinter as tk
from tkinter import messagebox
from systems.screenManagementSystem import ScreenManagementSystem

class ScreenModifyScreen:
    def __init__(self, root):
        self.root = root
        self.system = ScreenManagementSystem()

        self.current_screen_id = ""

        self.root.title("Screen Management Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_modify_screen)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_get_screen()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="SCREEN MANAGEMENT", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_delete = tk.Button(self.root, text="삭제하기", command=self.delete_screen)
        self.btn_modify = tk.Button(self.root, text="수정하기", command=self.update_screen)

        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")
        new_screen_number_label = tk.Label(self.root, text="새로운 스크린 번호:")
        new_seat_capacity_label = tk.Label(self.root, text="새로운 좌석 수:")
    
        self.entry_new_screen_number = tk.Entry(self.root)
        self.entry_new_seat_capacity = tk.Entry(self.root)

        self.result_display = tk.Text(self.root, height=5, width=50)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.result_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        new_screen_number_label.grid(row=2, column=0, sticky=tk.E)
        new_seat_capacity_label.grid(row=3, column=0, sticky=tk.E)
        self.entry_new_screen_number.grid(row=2, column=1, sticky=tk.W)
        self.entry_new_seat_capacity.grid(row=3, column=1, sticky=tk.W)
        self.btn_delete.grid(row=2, column=3, padx=10, sticky=tk.E)
        self.btn_modify.grid(row=3, column=3, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.btn_next.grid(row=4, column=3, padx=10, pady=10, sticky=tk.E)

    def perform_get_screen(self):
        self. search_results = self.system.get_screens()
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            screen = self.search_results[self.current_page]
            display_text = (
                f"Screen ID: {screen['screen_id']}\n\n"
                f"Screen Number: {screen['screen_number']}\n\n"
                f"Seat Capacity: {screen['seat_capacity']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_screen_id = screen['screen_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def delete_screen(self):
        try:
            if (self.current_screen_id):
                self.system.delete_screen(self.current_screen_id)
                messagebox.showinfo("Screen Modify Attempt", f"성공적으로 스크린 정보가 삭제되었습니다.")
            else:
                messagebox.showinfo("Screen Modify Attempt", f"스크린 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Screen Modify Attempt", f"스크린 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_screen()

    def update_screen(self):
        new_screen_number = self.entry_new_screen_number.get()
        new_seat_capacity = self.entry_new_seat_capacity.get()
        try:
            if (self.current_screen_id and new_screen_number and new_seat_capacity):
                self.system.update_screen(self.current_screen_id, new_screen_number, new_seat_capacity)
                messagebox.showinfo("Screen Modify Attempt", f"성공적으로 스크린 정보가 수정되었습니다.")
            else:
                messagebox.showinfo("Screen Modify Attempt", f"스크린 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Screen Modify Attempt", f"스크린 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_screen()

    def end_modify_screen(self):
        self.system.close()
        self.root.destroy()