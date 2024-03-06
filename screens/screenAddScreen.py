import tkinter as tk
from tkinter import messagebox
from systems.screenManagementSystem import ScreenManagementSystem

class ScreenAddScreen:
    def __init__(self, root):
        self.root = root
        self.system = ScreenManagementSystem()

        self.root.title("Screen Add Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_add_screen)

        self.create_widgets()


    def create_widgets(self):
        validate_command = (self.root.register(self.only_numbers), '%S')
        
        label_title = tk.Label(self.root, text="SCREEN ADD", justify=tk.CENTER)
        label_screen_number = tk.Label(self.root, text="Screen Number:")
        label_seat_capacity = tk.Label(self.root, text="Seat Capacity:")

        self.screen_number_entry = tk.Entry(self.root, validate='key', validatecommand=validate_command)
        self.seat_capacity_entry = tk.Entry(self.root, validate='key', validatecommand=validate_command)

        add_button = tk.Button(self.root, text="추가", command=self.attempt_add_screen)

        label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0))
        label_screen_number.grid(row=1, column=0, sticky=tk.E)
        self.screen_number_entry.grid(row=1, column=1, sticky=tk.W)
        label_seat_capacity.grid(row=2, column=0, sticky=tk.E)
        self.seat_capacity_entry.grid(row=2, column=1, sticky=tk.W)
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        
    def attempt_add_screen(self):
        screen_number = self.screen_number_entry.get()
        seat_capacity = self.seat_capacity_entry.get()
        
        try:
            self.system.add_screen(screen_number, seat_capacity)
            messagebox.showinfo("Add Screen Attempt", f"성공적으로 상영관을 추가하였습니다.")
        except Exception as e:
            messagebox.showinfo("Add Screen Attempt", f"상영관을 추가하는 과정에서 오류가 발생하였습니다.\n{e}")

    def only_numbers(self, char):
        return char.isdigit()

    def end_add_screen(self):
        self.system.close()
        self.root.destroy()