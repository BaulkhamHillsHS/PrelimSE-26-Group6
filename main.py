import customtkinter as ctk
import tkinter as tk

"""
Notes:
Login/welcome screen:
    - Components
    - Left: user creation screen 
        - Top: 'No account?' label (or something like that)
        - Bottom: 'Create an account' button
            In create account screen:
                - title label: 'create an account'
                - text boxes:
                    - name (needed?)
                    - username
                    - email
                    - password
                        - requirements: length, specal characters
                    - age (use this age as the default for new profiles, as well as default for auto created profile when creating an account)                
    - Right: list of users
        - Top: 'Existing accounts' label
        - Middle: combobox with a list of users
        - Bottom: 'continue' button to continue to login screen based on selected user
                  feedback label in case user has not selected 

once logged in, open settings by clicking on their pfp, 
have settings such as:
- profile management, list of profiles
    - switch profiles by clicking
    - delete profiles
    - create new profiles
  - each profile should have:
      - age
        - show nsfw?  (should be disabled when age < 18, toggle switch)
            - https://youtu.be/uGI0tkmyogU?t=1590 "We should blur this on YouTube and make it unblurred on Nebula."
      - watch history

"""

NAME = "yaoi"

class LoginFrame(ctk.CTkFrame):
    # Frame for log in/welcome screen
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logintitle = ctk.CTkLabel(self, text="login")
        self.logintitle.pack(pady=30)

        self.loginbtn = ctk.CTkButton(self, text="login", command=master.loggedin)
        self.loginbtn.pack(pady=50)


class MainFrame(ctk.CTkFrame): # better name than mainframe?
    # Frame for after login, watching things idk
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.maintitle = ctk.CTkLabel(self, text="main")
        self.maintitle.pack(pady=30)



class StreamingServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(NAME + " streaming service :3 ")
        self.geometry("720x720")
        
        self.accounts_list = [] # make csv soontm


        self.login = LoginFrame(self)
        self.login.pack()

        self.main = MainFrame(self)

        self.create_account_button = ctk.CTkButton(self, text="Create an account", command=self.create_signup_form)
        self.create_account_button.pack(pady=20)

        self.signup_form = None

    def loggedin(self):
        self.login.forget()
        self.main.pack()


    def create_signup_form(self):
        if self.signup_form is not None:
            return

        self.signup_form = ctk.CTkFrame(self)
        self.signup_form.pack(pady=10, padx=20, fill="both", expand=True)

        self.username_label = ctk.CTkLabel(self.signup_form, text="Username")
        self.username_label.pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(self.signup_form)
        self.username_entry.pack(pady=5)

        self.age_label = ctk.CTkLabel(self.signup_form, text="Age")
        self.age_label.pack(pady=(10, 0))
        self.age_entry = ctk.CTkEntry(self.signup_form)
        self.age_entry.pack(pady=5)

        self.email_label = ctk.CTkLabel(self.signup_form, text="Email")
        self.email_label.pack(pady=(10, 0))
        self.email_entry = ctk.CTkEntry(self.signup_form)
        self.email_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.signup_form, text="Password")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(self.signup_form, show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_label = ctk.CTkLabel(self.signup_form, text="Confirm password")
        self.confirm_password_label.pack(pady=(10, 0))
        self.confirm_password_entry = ctk.CTkEntry(self.signup_form, show="*")
        self.confirm_password_entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(self.signup_form, text="Submit", command=self.submit_account)
        self.submit_button.pack(pady=15)

        self.status_label = ctk.CTkLabel(self.signup_form, text="")
        self.status_label.pack()

    def submit_account(self):
        username = self.username_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if any(var == "" for var in (username, age, email, password, confirm_password)):
            self.status_label.configure(text="Please fill in all fields.", text_color="red")
            return
        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match.", text_color="red")
            return

        self.accounts_list.append([username, age, email, password])

        self.status_label.configure(text="Account created successfully!", text_color="green")

        print(self.accounts_list)


app = StreamingServiceApp()
app.mainloop()