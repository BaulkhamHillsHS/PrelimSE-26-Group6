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
        self.title(NAME + " streaming service")
        self.geometry("720x420")


        self.login = LoginFrame(self)
        self.login.pack()

        self.main = MainFrame(self)

    def loggedin(self):
        self.login.forget()
        self.main.pack()

    

app = StreamingServiceApp()
app.mainloop()