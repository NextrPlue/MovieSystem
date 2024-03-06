import tkinter as tk
from tkinter import messagebox
from systems.loginSystem import LoginSystem

class RegisterScreen:
    def __init__(self, root):
        self.root = root
        self.system = LoginSystem()

        self.root.title("Register Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 닫기 버튼 클릭 시 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.end_register)

        # 회원가입 화면 레이아웃 구성
        self.create_widgets()

    def create_widgets(self):
        label_title = tk.Label(self.root, text="Register", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text="PNU Movie에 오신 것을 환영합니다!\n회원정보를 입력해 주세요.\n", justify=tk.LEFT)
        label_name = tk.Label(self.root, text="이름:")
        label_email = tk.Label(self.root, text="ID:")
        label_password = tk.Label(self.root, text="PASSWORD:")
        label_password_confirm = tk.Label(self.root, text="Confirm PASSWORD:")
        label_phone = tk.Label(self.root, text="연락처:")

        self.entry_name = tk.Entry(self.root)
        self.entry_email = tk.Entry(self.root)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password_confirm = tk.Entry(self.root, show="*")
        self.entry_phone = tk.Entry(self.root)

        button_register = tk.Button(self.root, text="Register", command=self.attempt_register)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        label_welcome.grid(row=1, column=0, columnspan=2, pady=(5, 5))
        label_name.grid(row=2, column=0, sticky=tk.E)
        label_email.grid(row=3, column=0, sticky=tk.E)
        label_password.grid(row=4, column=0, sticky=tk.E)
        label_password_confirm.grid(row=5, column=0, sticky=tk.E)
        label_phone.grid(row=6, column=0, sticky=tk.E)
        self.entry_name.grid(row=2, column=1, sticky=tk.W)
        self.entry_email.grid(row=3, column=1, sticky=tk.W)
        self.entry_password.grid(row=4, column=1, sticky=tk.W)
        self.entry_password_confirm.grid(row=5, column=1, sticky=tk.W)
        self.entry_phone.grid(row=6, column=1, sticky=tk.W)
        button_register.grid(row=7, column=0, columnspan=2, pady=(5, 0))

    def attempt_register(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        password_confirm = self.entry_password_confirm.get()
        phone = self.entry_phone.get()
        
        flag = self.system.create_user(name, email, password, phone)

        if password != password_confirm:
            messagebox.showinfo("Register Attempt", f"비밀번호를 다시 확인해주세요.")
        elif flag == 1:
            messagebox.showinfo("Register Attempt", f"{name}님 정상적으로 회원가입 되었습니다!")
            self.end_register()
        elif flag == 2:
            messagebox.showinfo("Register Attempt", f"중복된 이메일이 존재합니다.")
        elif flag == 3:
            messagebox.showinfo("Register Attempt", f"회원가입이 정상적으로 수행되지 않았습니다.")
        else:
            self.end_register()

    def end_register(self):
        self.system.close()
        self.root.destroy()