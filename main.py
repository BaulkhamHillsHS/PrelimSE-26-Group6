from abc import ABC, abstractmethod
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
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(2, weight=2)

        self.signup_form = None
        self.buildui()

    def buildui(self):
        if self.signup_form:
            self.signup_form.destroy()
            self.signup_form = None
        self.logintitle = ctk.CTkLabel(self, text="login", font=("Roboto", 50))
        self.logintitle.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(30, 60))

        self.create_account_button = ctk.CTkButton(self, 300, 50, text="Create an account", command=self.create_signup_form)
        self.create_account_button.grid(row=2, column=0, sticky="nsew", padx=10)

        self.accountbox = ctk.CTkComboBox(self, values=self.master._accounts.get_usernames())
        self.accountbox.grid(row=1, column=1, padx=10, pady=10)

        self.loginbtn = ctk.CTkButton(self, 300, 50, text="login", command=self.master.loggedin)
        self.loginbtn.grid(row=2, column=1, sticky="nsew", padx=10)

        if self.master._accounts.get_usernames() == []:
            self.accountbox.set("No accounts")
            self.accountbox.configure(state="disabled")
            self.loginbtn.configure(state="disabled")


    def create_signup_form(self):
        self.create_account_button.grid_forget()
        self.loginbtn.grid_forget()
        self.accountbox.grid_forget()
        if self.signup_form == None:
            self.signup_form = SignupFrame(self)
            self.signup_form.grid(row=0, column=0, padx=15, pady=15, columnspan=2, rowspan=3, sticky="nesw")


class FormFrame(ctk.CTkFrame, ABC):
    """
    Default frame for forms\n
    Enter a title and a dictionary of values\n
    Dictionary should be in form {"entry name": "type"}\n
    "entry name" is the name of the label next to the box\n
    "type" is the type of entry\n
    valid types are "password" and "number"
    """
    def __init__(self, master, title, vars:dict={}, **kwargs):
        
        super().__init__(master, **kwargs)
        self.vars = vars
        self.length = len(vars)
        self.passwordids = []
        for i in range(self.length):
            if [*vars.values()][i] == "password":
                self.passwordids.append(i)


        self.grid_rowconfigure(self.length+4, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text=title)
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.entrys = []
        for i in range(self.length):
            label = ctk.CTkLabel(self, text=(t:=[*vars.keys()])[i])
            label.grid(row=i+1, column=0)
            if [*vars.values()][i] == "password":
                entry = ctk.CTkEntry(self, show="*")
            else:
                entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1)
            self.entrys.append(entry)

        
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.grid(row=self.length+1, column=0, columnspan=2)

        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=self.length+2, column=0, columnspan=2, pady=10)

        self.cancel_btn = ctk.CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_btn.grid(row=self.length+3, column=0, columnspan=2, pady=10)

    @abstractmethod
    def submit(self):
        self.values = []
        for i in range(self.length):
            self.values.append(value:=self.entrys[i].get())
            if value == "":
                self.status_label.configure(text="Please fill in all fields")
                return
            if [*self.vars.values()][i] == "number":
                try:
                    age = int(value)
                    if age <= 0:
                        raise ValueError
                except:
                    self.status_label.configure(text="Please enter a positive whole number for age")
                    return
            checkpassword = self.passwordids[1:]
            for i in range(len(checkpassword)):
                if self.passwordids[0] != checkpassword[i]:
                    self.status_label.configure(text="Passwords do not match.")
                    return

    @abstractmethod
    def cancel(self):
        pass
        

class SignupFrame(ctk.CTkFrame):
    # Frame to create an account
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text="Create an account")
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=1, column=0)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.age_label = ctk.CTkLabel(self, text="Age")
        self.age_label.grid(row=2, column=0)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_label.grid(row=3, column=0)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=4, column=0)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10)

        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm password")
        self.confirm_password_label.grid(row=5, column=0, padx=(10, 0))
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.grid(row=5, column=1, padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=6, column=0, columnspan=2)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_account)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.back_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_submit)
        self.back_button.grid(row=8, column=0, columnspan=2, pady=10)


    def submit_account(self):
        username = self.username_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if any(var == "" for var in (username, age, email, password, confirm_password)):
            self.status_label.configure(text="Please fill in all fields.", text_color="red")
            return
        
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except:
            self.status_label.configure(text="Please enter a positive whole number for age", text_color="red")
            return
        
        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match.", text_color="red")
            return

        if username in self.master.master._accounts.get_usernames():
            self.status_label.configure(text=f"Username {username} is taken.", text_color="red")
            return

        self.master.master._accounts.add_account(username, age, email, password)

        self.status_label.configure(text="Account created successfully!", text_color="green")

        print(self.master.master._accounts.get_usernames())
        self.master.master.newaccountloggedin()

    def cancel_submit(self):
        self.master.buildui()


class AccountInfoFrame(ctk.CTkFrame):
    # Frame for showing account information
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.accountnametxt = ctk.CTkLabel(self, text="Account: "+self.master.master.account)
        self.accountnametxt.grid(row=0, column=0)

        self.profilelist = ctk.CTkComboBox(self, values=self.master.master.profiles)
        self.profilelist.grid(row=1, column=0)

        self.newprofilebtn = ctk.CTkButton(self, text="New Profile")
        self.newprofilebtn.grid(row=2, column=0)

        self.switchprofilebtn = ctk.CTkButton(self, text="Switch Profile")
        self.switchprofilebtn.grid(row=3, column=0)

        self.logoutbtn = ctk.CTkButton(self, text="Logout", command=master.master.logout)
        self.logoutbtn.grid(row=4, column=0)




class ProfileFrame(ctk.CTkFrame):
    # profile name, age
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(10, weight=1)

        self.title = ctk.CTkLabel(self, text="Create a profile")
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.username_label = ctk.CTkLabel(self, text="Profile name")
        self.username_label.grid(row=1, column=0)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.age_label = ctk.CTkLabel(self, text="Age")
        self.age_label.grid(row=2, column=0)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)



class MainFrame(ctk.CTkFrame): # better name than mainframe?
    # Frame for after login, watching things idk
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(10, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.maintitle = ctk.CTkLabel(self, text="main")
        self.maintitle.grid(row=0, column=0, padx=10, pady=10)

        self.profilebtn = ctk.CTkButton(self, text="", width=60, height=60, corner_radius=30, command=self.toggle_account_info_visibility)
        self.profilebtn.grid(row=0, column=10)

        self.accountinfo = AccountInfoFrame(self)

    def updateaccount(self, account):
        self.accountinfo.accountnametxt.configure(text="Account: "+account)

    def toggle_account_info_visibility(self):
        if self.accountinfo.winfo_ismapped():
            self.accountinfo.grid_forget()
        else:
            self.accountinfo.grid(row=1, column=8, rowspan=3, columnspan=3)




class StreamingServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(NAME + " streaming service :3 ")
        self.geometry("720x720")

        self._accounts = UserAccounts()
        self.account = ""
        self.profile = ""
        self.profiles = self._accounts.get_profiles(self.account)

        self.titletxt = ctk.CTkLabel(self, text=NAME, text_color="pink")
        self.titletxt.pack(side="top", pady=(40, 0))

        self.login = LoginFrame(self)
        self.login.pack(fill="both", expand=True, padx=40, pady=40)

        self.main = MainFrame(self)

        self.profile = ProfileFrame(self)

    def loggedin(self):
        self.changeframetomain()
        self.account = self.login.accountbox.get()
        self.main.updateaccount(self.account)

    def newaccountloggedin(self):
        self.changeframetomain()
        self.account = self.login.signup_form.username_entry.get()
        self.main.updateaccount(self.account)

    def logout(self):
        self.changeframetologin()
        self.login.pack()
        self.login.buildui()
        self.account = ""

    def changeframetomain(self):
        self.login.create_account_button.grid_forget()
        self.login.accountbox.grid_forget()
        self.login.loginbtn.grid_forget()
        self.login.forget()
        self.main.pack(fill="both", expand=True)

    def changeframetologin(self):
        self.main.forget()
        self.main.accountinfo.grid_forget()

    def changeframetoprofile(self):
        pass

    



class UserAccounts:
    # Only handles data
    FIELDS = ["username", "age", "email", "password", "profiles"]

    def __init__(self):
        self._accounts = []

    def add_account(self, username, age, email, password, profiles:list=[]):
        self._accounts.append({"username": username,
                               "age": age,
                               "email": email,
                               "password": password,
                               "profiles": profiles})
        self._refresh()
    
    def remove_account(self, username):
        self._accounts.remove(username)
        self._refresh()

    def get_usernames(self):
        return [*map(lambda user: user["username"], self._accounts)]
    
    def get_profiles(self, username):
        return self._accounts[self._accounts.index(username)]["profiles"] if username else []
    
    def _refresh(self):
        # Updates the values
        self.usernames = self.get_usernames()
        
        


app = StreamingServiceApp()
app.mainloop()