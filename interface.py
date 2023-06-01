import customtkinter
import pyautogui as pg
from functools import partial
import threading 
import time

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("LAND Helper")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.frame_pass = None
#        self.grid_num = 1

        self.data_dict = {
#            None: print
            }

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="LAND", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text='Основное', command=partial(self.common_frame,'main',True))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,text='Войти', command=partial(self.common_frame,'login'))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame,text='Настройки', command=partial(self.common_frame,'setting'))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.common_frame('main',True)
    def wait_game(self):    
        @thread
        def func_wait_game():
            x = 0
            while True:
                if not self.data_dict.get('need_wait',True):
                    break
                if x%5==0:
                    pg.click(950,788)
                _time = f'Прошло {x//60} минут'
                self.time_label.configure(text=_time)
                time.sleep(1)
                x +=1 
        @thread
        def get_str_seg_btn(*arg):
            if arg[0] == 'Прекратить ожидание игры':
                self.progressbar_1.stop()
                self.time_label.configure()
                self.data_dict['need_wait']=False
            if arg[0] == 'Ожидание игры':
                self.progressbar_1.start()
                self.data_dict['need_wait']=True
                func_wait_game()
        def close():
            self.data_dict.pop('mini_menu',None)
            self.slider_progressbar_frame.destroy()
            self.switch.deselect()
        if self.switch.get() != 0:    
            if self.data_dict.get('mini_menu',None) is not None:
                return
            else:
                self.data_dict['mini_menu'] = True
                self.slider_progressbar_frame = customtkinter.CTkFrame(self.frame)
                self.slider_progressbar_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
                self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
                self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
                self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame,command=get_str_seg_btn)
                self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
                self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
                self.progressbar_1.configure(mode="indeterminnate")
                self.progressbar_1.start()
                self.seg_button_1.configure(values=["Ожидание игры",'Прекратить ожидание игры'])
                self.seg_button_1.set("Ожидание игры")
                self.time_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Прошло 0 минут", font=customtkinter.CTkFont(size=20, weight="bold"))
                self.time_label.grid(row=3, column=0, padx=20, pady=(20, 10))
                self.button = customtkinter.CTkButton(self.slider_progressbar_frame,text='Закрыть меню',fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=close)
                self.button.grid(row=10, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew") 
                func_wait_game()
        else:
            close()
    def common_frame(self,__name:str,__sticky=False):
        def close():
            self.data_dict.clear()
            self.frame.destroy()
        if self.data_dict.get('menu',None) is not None:
            close()
        self.data_dict['menu'] = True
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=1, column=1, padx=20, pady=20,sticky="nsew" if __sticky == True else 'n')
        self.frame.grid_columnconfigure(1, weight=1)
        if __name == 'login':
            self.logo_label = customtkinter.CTkLabel(self.frame, text="Авторизация", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.user_login = customtkinter.CTkEntry(self.frame, placeholder_text="Логин")  
            self.user_login.grid(row=3, column=0,  padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.user_password = customtkinter.CTkEntry(self.frame, placeholder_text="Пароль")
            self.user_password.grid(row=4, column=0,  padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.login_button = customtkinter.CTkButton(self.frame,text='Войти',command=lambda :print)
            self.login_button.grid(row=5, column=0, padx=(20, 20), pady=(20, 20))

        elif __name == 'main':
            self.logo_label = customtkinter.CTkLabel(self.frame, text="Основное меню", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10))
            
            self.scrollable_frame = customtkinter.CTkScrollableFrame(self.frame, label_text="Команды:")
            self.scrollable_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=1)
            self.scrollable_frame_switches = []
            self.switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Ожидание игры",command=self.wait_game)
            self.switch.grid(row=0, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(self.switch)

        elif __name == 'setting':
            self.label = customtkinter.CTkLabel(self.frame, text="Настройки", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.label.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.appearance_mode_label = customtkinter.CTkLabel(self.frame, text="Тема приложения:", anchor="w")
            self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame, values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode_event)
            self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
            self.scaling_label = customtkinter.CTkLabel(self.frame, text="Размер приложения:", anchor="w")
            self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
            self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        close_button = customtkinter.CTkButton(self.frame,text='Закрыть',command=close)
        close_button.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))
        return self.frame
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)



if __name__ == "__main__":
    app = App()
    app.mainloop()