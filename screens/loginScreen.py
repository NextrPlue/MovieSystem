import tkinter as tk
from tkinter import messagebox
from systems.loginSystem import LoginSystem

class LoginScreen:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.system = LoginSystem()

        self.root.title("Login Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_login)

        # 로그인 화면 레이아웃 구성
        self.create_widgets()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="LOGIN", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text="다시 오신 것을 환영합니다!\n아이디와 비밀번호를 입력해 주세요.", justify=tk.LEFT)
        label_email = tk.Label(self.root, text="ID:")
        label_password = tk.Label(self.root, text="PASSWORD:")

        self.entry_email = tk.Entry(self.root)
        self.entry_password = tk.Entry(self.root, show="*")

        button_login = tk.Button(self.root, text="Login", command=self.attempt_login)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        label_welcome.grid(row=1, column=0, columnspan=2, pady=(5, 5))
        label_email.grid(row=2, column=0, sticky=tk.E)
        label_password.grid(row=3, column=0, sticky=tk.E)
        self.entry_email.grid(row=2, column=1, sticky=tk.W)
        self.entry_password.grid(row=3, column=1, sticky=tk.W)
        button_login.grid(row=4, column=0, columnspan=2, pady=(5, 0))

    def attempt_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        self.user = self.system.get_user(email, password)

        if self.user:
            self.user = self.user[0]
            messagebox.showinfo("Login Attempt", f"{self.user[1]}님 다시 오신 것을 환영합니다!")
            self.end_login()
            self.on_success_callback(self.user)
        else:
            messagebox.showinfo("Login Attemnt", f"로그인에 실패하였습니다.\n아이디 및 비밀번호를 다시 확인해주세요.")

    def end_login(self):
        self.system.close()
        self.root.destroy()