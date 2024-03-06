import tkinter as tk
from screens.homeScreen import HomeScreen
from screens.mainScreen import MainScreen

app = None

def main():
    global app
    root = tk.Tk()
    app = HomeScreen(root, on_login_success)
    root.mainloop()

def on_login_success(user_data):
    # 로그인 성공 후 MainScreen으로 전환
    global app
    print(user_data)
    app.close_screen()
    root = tk.Tk()
    app = MainScreen(root, user_data)  # MainScreen 인스턴스 생성, 사용자 데이터 전달
    root.mainloop()

main()