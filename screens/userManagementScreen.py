import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from systems.userManagementSystem import UserManagementSystem

class UserManagementScreen:
    def __init__(self, root):
        self.root = root
        self.system = UserManagementSystem()

        self.current_user_id = ""

        self.root.title("User Management Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_user_management)        

        # 검색 결과와 페이지 관련 변수
        self.search_results = []  # 검색 결과를 저장할 리스트
        self.current_page = 0  # 현재 페이지 번호

        self.create_widgets()
        self.perform_get_user()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="USER MANAGEMENT", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_delete = tk.Button(self.root, text="삭제하기", command=self.delete_user)
        self.btn_modify = tk.Button(self.root, text="수정하기", command=self.update_user)

        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")
        new_user_role_label = tk.Label(self.root, text="새로운 역할:")
    
        self.user_role_combobox = ttk.Combobox(self.root, 
                                               values=["customer", "admin", "distributor"],
                                               state="readonly")  # 사용자가 입력하는 것을 막고 선택만 가능하도록 설정
        self.user_role_combobox.set("customer")  # 기본값 설정

        self.result_display = tk.Text(self.root, height=9, width=50)

        label_title.grid(row=0, column=1, columnspan=2, pady=(5, 0))
        self.result_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        new_user_role_label.grid(row=2, column=0, sticky=tk.E)
        self.user_role_combobox.grid(row=2, column=1, sticky=tk.W)
        self.btn_modify.grid(row=2, column=2, padx=10, sticky=tk.E)
        self.btn_delete.grid(row=2, column=3, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)
        self.btn_next.grid(row=4, column=3, padx=10, pady=10, sticky=tk.E)

    def perform_get_user(self):
        self. search_results = self.system.get_all_users()
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            user = self.search_results[self.current_page]
            display_text = (
                f"User ID: {user['user_id']}\n\n"
                f"Name: {user['name']}\n\n"
                f"Email: {user['email']}\n\n"
                f"Phone Number: {user['phone_number']}\n\n"
                f"User role: {user['user_role']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_user_id = user['user_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def delete_user(self):
        try:
            if (self.current_user_id):
                self.system.delete_user(self.current_user_id)
                messagebox.showinfo("User Delete Attempt", f"성공적으로 사용자 정보가 삭제되었습니다.")
            else:
                messagebox.showinfo("User Delete Attempt", f"사용자 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("User Delete Attempt", f"사용자 정보 삭제 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_user()

    def update_user(self):
        new_user_role = self.user_role_combobox.get()
        try:
            if (self.current_user_id, new_user_role):
                self.system.update_user_role(self.current_user_id, new_user_role)
                messagebox.showinfo("User Update Attempt", f"성공적으로 사용자 정보가 수정되었습니다.")
            else:
                messagebox.showinfo("User Update Attempt", f"사용자 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("User Update Attempt", f"사용자 정보 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_user()

    def end_user_management(self):
        self.system.close()
        self.root.destroy()