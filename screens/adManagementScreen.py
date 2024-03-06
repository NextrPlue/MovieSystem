import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from systems.adManagementSystem import AdManagerSystem

class AdManagementScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.system = AdManagerSystem()

        self.current_advertisement_id = ""

        self.root.title("Advertisement Management Advertisement")

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
        label_title = tk.Label(self.root, text="ADVERTISEMENT MANAGEMENT", justify=tk.CENTER)

        self.btn_prev = tk.Button(self.root, text="이전", command=self.show_prev_page)
        self.btn_next = tk.Button(self.root, text="다음", command=self.show_next_page)
        self.btn_add = tk.Button(self.root, text="추가하기", command=self.add_advertisement)
        self.btn_delete = tk.Button(self.root, text="삭제하기", command=self.delete_advertisement)

        self.page_number_label = tk.Label(self.root, text=f"Page {self.current_page + 1}")
        movie_title_label = tk.Label(self.root, text="추가할 영화 제목:")
    
        self.movie_combobox = ttk.Combobox(self.root, state="readonly")
    
        self.movie_combobox.bind("<<ComboboxSelected>>")
    
        self.result_display = tk.Text(self.root, height=9, width=50)

        label_title.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.result_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        movie_title_label.grid(row=2, column=0, sticky=tk.E)
        self.movie_combobox.grid(row=2, column=1, sticky=tk.W)
        self.btn_add.grid(row=2, column=3, padx=10, sticky=tk.E)
        self.btn_delete.grid(row=3, column=3, padx=10, sticky=tk.E)
        self.btn_prev.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.page_number_label.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.btn_next.grid(row=4, column=3, padx=10, pady=10, sticky=tk.E)

        # 콤보박스에 데이터 채우기
        self.load_movies()

    def perform_get_screen(self):
        self. search_results = self.system.get_advertisements_by_user(self.user[0])
        self.current_page = 0
        self.show_current_page()

    def load_movies(self):
        movies = self.system.get_movies()
        # movie_id와 title을 매핑하는 딕셔너리 생성
        self.movie_id_title_map = {title: movie_id for title, movie_id in movies}
        # 콤보박스에 영화 제목을 채움
        self.movie_combobox['values'] = [title for title, movie_id in movies]
        self.movie_combobox.set('영화 선택')

    def show_current_page(self):
        # 현재 페이지의 단일 검색 결과 표시
        self.result_display.delete('1.0', tk.END)

        if self.current_page < len(self.search_results):
            advertisement = self.search_results[self.current_page]
            display_text = (
                f"Advertisement ID: {advertisement['advertisement_id']}\n\n"
                f"Title: {advertisement['title']}\n\n"
                f"Director: {advertisement['director']}\n\n"
                f"Genre: {advertisement['genre']}\n\n"
                f"Release Date: {advertisement['release_date']}"
            )
            self.result_display.insert(tk.END, display_text)
            self.current_advertisement_id = advertisement['advertisement_id']
        self.page_number_label.config(text=f"Page {self.current_page + 1}")

    def show_next_page(self):
        if self.current_page < len(self.search_results) - 1:
            self.current_page += 1
            self.show_current_page()

    def show_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def delete_advertisement(self):
        try:
            if (self.current_advertisement_id):
                self.system.delete_advertisement(self.current_advertisement_id)
                messagebox.showinfo("Advertisement Modify Attempt", f"성공적으로 광고 정보가 삭제되었습니다.")
            else:
                messagebox.showinfo("Advertisement Modify Attempt", f"광고 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Advertisement Modify Attempt", f"광고 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_screen()

    def add_advertisement(self):
        movie_title = self.movie_combobox.get()
        
        try:
            if (movie_title != "영화 선택"):
                movie_id = self.movie_id_title_map[movie_title]
                self.system.add_advertisement(self.user[0], movie_id)
                messagebox.showinfo("Advertisement Modify Attempt", f"성공적으로 광고 정보가 추가되었습니다.")
            else:
                messagebox.showinfo("Advertisement Modify Attempt", f"영화 정보가 없습니다.")
        except Exception as e:
            messagebox.showinfo("Advertisement Modify Attempt", f"광고 수정 과정에서 오류가 발생하였습니다.\n{e}")
        self.perform_get_screen()

    def end_modify_screen(self):
        self.system.close()
        self.root.destroy()