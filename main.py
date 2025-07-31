import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
import html
import os

import authenticated
import unauthenticated
import general
 

basedir = os.path.dirname(__file__)
user_authenticated = False

current_page = ''
 
class Main:
    def __init__(self):
        global user_authenticated
        global current_page
        

        self.root = ctk.CTk()

        self.root.iconbitmap(os.path.join(basedir, "mandelbrot.ico"))

        theme = general.get_theme()
        
        ctk.set_appearance_mode(theme)


        self.root.geometry('800x500')
        self.root.title('mandelbrotCMS light')
    
        self.header = ctk.CTkFrame(self.root)
        
        
        self.home_btn = ctk.CTkButton(self.header, text='Home', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.nav_home)
        self.created_lists_btn = ctk.CTkButton(self.header, text='Created Lists', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.nav_lists)
        self.new_list_btn = ctk.CTkButton(self.header, text='New List', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.nav_create_list) 


        self.theme_btn = ctk.CTkButton(self.header, text=theme.capitalize() if theme == 'light' or theme == 'dark' else 'theme', font=('Arial', 16), width=1, fg_color=('gray95','gray10'), text_color=('gray15', 'white'), command=self.handle_change_theme)
        
        self.seperator_1 = ctk.CTkFrame(self.header, width=1, bg_color=('gray15', 'white'), height=20)
        self.seperator_2 = ctk.CTkFrame(self.header, width=1, bg_color=('gray15', 'white'), height=20)
        self.seperator_3 = ctk.CTkFrame(self.header, width=1, bg_color=('gray15', 'white'), height=20)

        self.header_seperator = ctk.CTkFrame(self.root, height=1, bg_color=('gray15', 'white'))

        self.parent_container = ctk.CTkFrame(self.root)


        self.header.pack(fill='x', side='top')

        self.home_btn.pack(side='left', padx=(20, 0), pady=5)
        self.seperator_1.pack(side='left', padx=5)
        self.created_lists_btn.pack(side='left', pady=5)
        self.seperator_2.pack(side='left', padx=5)
        self.new_list_btn.pack(side='left', pady=5)
        self.seperator_3.pack(side='left', padx=5)


        self.theme_btn.pack(side='right', padx=(0, 20), pady=5)

        self.header_seperator.pack(fill='x', padx=20)

        self.parent_container.pack(fill='both', expand=True)

        user_authenticated = authenticated.set_creds()

        if user_authenticated:
            self.logout_btn = ctk.CTkButton(self.header, text='Logout', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.handle_logout)
            self.logout_btn.pack(side='left', pady=5)
        else:
            self.login_btn = ctk.CTkButton(self.header, text='Login', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.nav_login)
            self.login_btn.pack(side='left', pady=5)
            

        self.nav_home()

    
    def clear_parent(self):
        for child in self.parent_container.winfo_children():
            child.destroy()

        return
    
    def nav_home(self, force=False):
        global current_page
        if not force and current_page == 'home':
            return

        self.clear_parent()

        Home(self.parent_container)
        current_page = 'home'


    def nav_create_list(self):
        global current_page
        if current_page == 'create_list':
            return
        
        self.clear_parent()

        CreateList(self.parent_container)
        current_page = 'create_list'


    def nav_lists(self):
        global current_page
        if current_page == 'lists':
            return
        
        self.clear_parent()

        Lists(self.parent_container)
        current_page = 'lists'


    def nav_login(self):
        global current_page
        if current_page == 'login':
            return
        
        self.clear_parent()

        Login(self.parent_container, self.login_btn)
        current_page = 'login'

    def handle_logout(self):
        global user_authenticated

        authenticated.logout()

        self.logout_btn.destroy()
        self.login_btn = ctk.CTkButton(self.header, text='Login', font=('Arial', 16), width=1, fg_color='transparent', text_color=('gray15', 'white'), command=self.nav_login)
        self.login_btn.pack(side='left', pady=5)

        user_authenticated = False
        CTkMessagebox(title='Logged Out!', message='You Successfully Logged Out!', icon='check', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)
        self.nav_home(force=True)

    def handle_change_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == 'Dark':
            ctk.set_appearance_mode('light')
            general.set_theme('light')

            self.theme_btn.configure(text='Light')

        if current_mode == 'Light':
            ctk.set_appearance_mode('dark')
            general.set_theme('dark')

            self.theme_btn.configure(text='Dark')


    def run(self):
        self.root.mainloop()


class Home:
    today_list = {'title': '', 'tasks': []}
    def __init__(self, master):
        self.handle_get_list()

        self.container = ctk.CTkFrame(master, fg_color='transparent')
        self.container.pack(fill='both', padx=30, pady=20)

        self.list_title = ctk.CTkLabel(self.container, text=self.today_list['title'], text_color=('gray15', 'white'), font=('Arial', 22), width=1, height=1, fg_color='transparent')
        self.list_title.pack(anchor='nw', pady=(0, 10))

        self.missions_container = ctk.CTkFrame(self.container, fg_color='transparent')
        self.missions_container.pack(fill='both')

        if len(self.today_list['missions']) == 0:
            self.list_title.configure(text="There is no created list for today.")       
        
        for mission in self.today_list['missions']:
            mission_frame = ctk.CTkFrame(self.missions_container)
            sep = ctk.CTkFrame(self.missions_container, height=1, bg_color=('gray15', 'white'))
            mission_content = ctk.CTkLabel(mission_frame, text=mission['content'], text_color=('gray15', 'white'), font=('Arial', 16))
            mission_content.pack(side='left', padx=20, pady=10)

            checkbox = ctk.CTkCheckBox(mission_frame,text='', width=1, height=1, border_width=2, corner_radius=100)
            checkbox.configure(command=lambda m_id=mission['id'], mission=mission: self.handle_update_mission(m_id, mission))
            
            checkbox.pack(side='right', padx=10, pady=10)
            if mission['status'] == 'done':
                checkbox.select()

            mission_frame.pack(side='top', fill='x')
            sep.pack(side='top', fill='x')
    
    
    def handle_get_list(self):
        global user_authenticated
        if user_authenticated:
            today_list = authenticated.get_today_list()
            if today_list != -1:
                self.today_list = today_list
            
            elif today_list == -1:
                user_authenticated = False
                self.today_list = unauthenticated.get_today_list()

        else:
            self.today_list = unauthenticated.get_today_list()

    def handle_update_mission(self, mission_id, mission):
        global user_authenticated

        statement = 'pending' if mission['status'] == 'done' else 'done'

        if user_authenticated:
            response = authenticated.update_mission(mission_id, data={'status': statement})
            
        else:
            response = unauthenticated.update_mission(mission_id, 'status', statement)

        if response == 1:
            mission['status'] = statement




class Lists:
    def __init__(self, master):
        self.container = ctk.CTkScrollableFrame(master, fg_color='transparent')
        self.container.pack(fill='both',pady=20, expand=True)

        self.handle_get_lists()

        for created_list in self.created_lists:
            list_container = ctk.CTkFrame(self.container, border_width=1, border_color=('gray15', 'white'), corner_radius=5)
            list_container.pack(fill='x', side='top', padx=30, pady=(0, 25))

            list_title = ctk.CTkLabel(list_container, text=created_list[self.keys['title']], font=('Arial', 22), text_color=('gray15', 'white'))
            list_title.pack(side='left', padx=15, pady=15)



    def handle_get_lists(self):
        global user_authenticated

        if user_authenticated:
            self.created_lists, self.keys = authenticated.get_lists()
        else:
            self.created_lists, self.keys = unauthenticated.get_lists()



class CreateList:

    data = []

    def __init__(self, master):
        self.container = ctk.CTkScrollableFrame(master, fg_color='transparent')
        self.container.pack(fill='both', expand=True, pady=20, padx=30)

        self.title_container = ctk.CTkFrame(self.container, fg_color='transparent')
        self.title_container.pack(anchor='nw')

        self.title_label = ctk.CTkLabel(self.title_container, text="List Title", font=('Arial', 22), text_color=('gray15', 'white'))
        self.title_label.pack(anchor='nw')

        self.title_field = ctk.CTkEntry(self.title_container, font=('Arial', 16))
        self.title_field.pack(anchor='nw', pady=(10, 0))

        self.missions_container = ctk.CTkFrame(self.container, fg_color='transparent', height=1)
        self.missions_container.pack(anchor='nw', pady=(30, 0))

        self.label_container = ctk.CTkFrame(self.missions_container, fg_color='transparent')
        self.label_container.pack(anchor='nw')
        
        self.missions_label = ctk.CTkLabel(self.label_container, text='Add Mission', font=('Arial', 22), text_color=('gray15', 'white'))
        self.missions_label.pack(side='left', padx=(0, 10))

        self.mission_add_btn = ctk.CTkButton(self.label_container, text='+', font=('Arial', 22), text_color=('gray15', 'white'),  fg_color='transparent', width=1, height=1,command=self.add_mission_form)
        self.mission_add_btn.pack(side='left', padx=(10, 0)) 

        self.missions = ctk.CTkFrame(self.missions_container, fg_color='transparent', height=1)
        self.missions.pack(anchor='nw')

        self.date_container = ctk.CTkFrame(self.container, fg_color='transparent')
        self.date_container.pack(anchor='nw', pady=(30, 0))

        self.date_label = ctk.CTkLabel(self.date_container, text='Date', font=('Arial', 22), text_color=('gray15', 'white'))
        self.date_label.pack(anchor='nw')

        self.date_field = DateEntry(self.date_container, font=('Arial', 12), width=10)
        self.date_field.pack(anchor='nw', pady=(10, 0))

        self.submit_container = ctk.CTkFrame(self.container, fg_color='transparent')
        self.submit_container.pack(anchor='nw', pady=(30, 0))
        
        self.submit_btn = ctk.CTkButton(self.submit_container, text='Create List', font=('Arial', 18), text_color=('gray15', 'white'), fg_color=('gray95', 'gray10'), width=1, command=self.handle_submit_list)
        self.submit_btn.pack(anchor='nw')


    def add_mission_form(self):
        self.mission_form_container = ctk.CTkFrame(self.missions, border_width=2, border_color='gray50', corner_radius=10)
        self.mission_form_container.pack(anchor='nw', padx=15, pady=15)

        self.content_field = ctk.CTkTextbox(self.mission_form_container, font=('Arial', 14), height=80)
        self.content_field.pack(side='left', padx=10, pady=10)

        btns_container = ctk.CTkFrame(self.mission_form_container, fg_color='transparent')
        btns_container.pack(side='right', anchor='se', padx=(60, 10), pady=10)
        
        cancel_btn = ctk.CTkButton(btns_container, width=1, text='cancel', font=('Arial', 14), text_color=('gray15', 'white'), fg_color=('gray95','gray10'), command=lambda: self.mission_form_container.destroy())
        add_btn = ctk.CTkButton(btns_container, width=1, text='add', font=('Arial', 14), text_color=('gray15', 'white'), fg_color=('gray95','gray10'), command=self.add_mission)
        
        cancel_btn.pack(side='left', padx=5)
        add_btn.pack(side='left', padx=5)


    def add_mission(self):
        self.data.append({'content': self.content_field.get('1.0', 'end')})

        self.mission_form_container.destroy()

        new_mission = ctk.CTkFrame(self.missions, fg_color='transparent')
        new_mission.pack(fill='x', side='top')

        mission_content = ctk.CTkLabel(new_mission, text=f"{html.unescape('&bull;')}  {self.data[-1]['content']}", font=('Arial', 16), text_color=('gray15', 'white'))
        mission_content.pack(side='left', padx=10, pady=(5, 0))


    def handle_submit_list(self):
        global user_authenticated

        list_title = self.title_field.get()
        list_date = str(self.date_field.get_date())
        missions = self.data

        if user_authenticated:
            response = authenticated.create_list({'title': list_title, 'date': list_date}, missions)
        else:
            response = unauthenticated.create_list({'title': list_title, 'date': list_date}, missions)

        if response == 1:
            CTkMessagebox(title='Successfully Created!', message='Missions List Successfully Created!', icon='check', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)
        elif response == 0 or response == -1:
            CTkMessagebox(title='Failed', message='Failed to Create Missions List.', icon='cancel', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)



class Login(Main):
    def __init__(self, master, login_btn):
        self.parent_container = master
        self.login_btn = login_btn
        self.container = ctk.CTkFrame(master, fg_color='transparent')
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.label = ctk.CTkLabel(self.container, text='Login', text_color=('gray15', 'white'), font=('Arial', 22))
        self.label.pack(anchor='nw')

        self.email_input = ctk.CTkEntry(self.container, width=200, height=25, placeholder_text='email', font=('Arial', 14))
        self.passsword_input = ctk.CTkEntry(self.container, show='*', width=200, height=25, placeholder_text='password', font=('Arial', 14))

        self.submit_btn = ctk.CTkButton(self.container, width=1, text='login', text_color=('gray15', 'white'), fg_color=('gray95', 'gray10'), font=('Arial', 16), command=self.handle_login)

        self.email_input.pack(pady=10)
        self.passsword_input.pack(pady=10)
        self.submit_btn.pack(anchor='center', pady=10)


    def handle_login(self):
        email_content = self.email_input.get()
        password_content = self.passsword_input.get()

        response = unauthenticated.login(email_content, password_content)

        if type(response) == bool and response:
            global user_authenticated

            user_authenticated = authenticated.set_creds()

            if user_authenticated:
                self.login_btn.configure(text='Logout', command=self.handle_logout)

                CTkMessagebox(title='Logged In!', message='You Successfully Logged In!', icon='check', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)
            else:
                CTkMessagebox(title='Failed', message='Failed to Log In', icon='cancel', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)
        else:
            CTkMessagebox(title='Failed', message=response, icon='cancel', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)

    def handle_logout(self):
        global user_authenticated

        authenticated.logout()
        self.login_btn.configure(text='Login', command=self.nav_login)


        user_authenticated = False
        CTkMessagebox(title='Logged Out!', message='You Successfully Logged Out!', icon='check', option_1='Ok', fg_color=('gray95', 'gray15'), text_color=('gray15', 'white'), sound=True)
        self.nav_home()

    def nav_home(self):
        global current_page
        self.clear_parent()

        Home(self.parent_container)
        current_page = 'home'

    def nav_login(self):
        global current_page
        self.clear_parent()

        Login(self.parent_container, self.login_btn)
        current_page = 'login'

    def clear_parent(self):
        for child in self.parent_container.winfo_children():
            child.destroy()

        return

Main().run()