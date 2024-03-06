import tkinter as tk
from .loginScreen import LoginScreen
from .registerScreen import RegisterScreen

class HomeScreen:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.root.title("Home Screen")

        # 창 크기 고정 및 창 크기 조정
        self.root.resizable(False, False)

        # 홈 화면 레이아웃 구성
        self.create_widgets()

    def open_login_screen(self):
        self.login_window = tk.Toplevel(self.root)  # 새 창 생성
        login_app = LoginScreen(self.login_window, self.on_login_success)  # LoginScreen 인스턴스 생성
        self.login_window.grab_set()  # 새 창에 대한 입력 포커스

    def open_register_screen(self):
        self.register_window = tk.Toplevel(self.root)  # 새 창 생성
        register_app = RegisterScreen(self.register_window)  # RegisterScreen 인스턴스 생성
        self.register_window.grab_set()  # 새 창에 대한 입력 포커스

    def close_screen(self):
        self.root.destroy()  # 창 닫기

    def on_login_success(self, user_data):
        print("로그인 성공, 홈 화면")
        self.on_success_callback(user_data)

    def create_widgets(self):
        label_title = tk.Label(self.root, text="WELCOME TO PNU MOVIE", justify=tk.CENTER)
        label_welcome = tk.Label(self.root, text="PNU MOVIE에 오신 것을 환영합니다!\n카테고리를 선택하여 주십시오.", justify=tk.LEFT)
        
        button1 = tk.Button(self.root, text="로그인", command=self.open_login_screen)
        button2 = tk.Button(self.root, text="회원가입", command=self.open_register_screen)
        button3 = tk.Button(self.root, text="종료", command=self.close_screen)

        # grid를 사용한 위젯 배치
        label_title.pack(pady=(5, 0))
        label_welcome.pack(pady=(5, 5))
        button1.pack(fill=tk.X, padx=10, pady=5)
        button2.pack(fill=tk.X, padx=10, pady=5)
        button3.pack(fill=tk.X, padx=10, pady=5)