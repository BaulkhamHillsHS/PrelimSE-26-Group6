from abc import ABC, abstractmethod
import csv
import CTkColorPicker as ctkcolor # pip install ctkcolorpicker
import customtkinter as ctk
from datetime import datetime
from PIL import Image # pip install Pillow
import tkinter as tk

"""
Notes:
NEEDED THINGS
profiles: 
- each profile should have an age, watch list and watch history
- profile should be a class

subscription management:
button next to profile to open a seperate window to see subscription and manage

OOP PROGRAMMING:
CONGposition - class containing classes 
- make a profile class, where the account class is containing profiles

encapsulation - more protected things? currently only _accounts

polymorphism - multiple classes containing same method
- easy imo, because video and tv show are going to be inheriting from the same abstract class









https://youtu.be/uGI0tkmyogU?t=1590 "We should blur this on YouTube and make it unblurred on Nebula."
"""

NAME = "yaoi"

class LoginFrame(ctk.CTkFrame):
    # Frame for log in/welcome screen
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(5, weight=2)
        self.grid_columnconfigure(2, weight=2)

        self.signup_form = None
        self.buildui()

    def buildui(self):
        """Builds the ui for signup form"""
        if self.signup_form:
            self.signup_form.destroy()
            self.signup_form = None
        self.logintitle = ctk.CTkLabel(self, text="Login", font=("Roboto", 50))
        self.logintitle.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(30, 60))

        self.create_account_button = ctk.CTkButton(self, 300, 50, text="Create an account", command=self.create_signup_form)
        self.create_account_button.grid(row=2, column=0, sticky="nsew", padx=10)

        self.accountbox = ctk.CTkEntry(self, placeholder_text="Username or Email", width=280)
        self.accountbox.grid(row=1, column=1, padx=10, pady=10)

        self.passwordbox = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=280)
        self.passwordbox.grid(row=2, column=1)

        self.feedback = ctk.CTkLabel(self, text="", text_color="red")
        self.feedback.grid(row=3, column=1)

        self.loginbtn = ctk.CTkButton(self, 300, 50, text="Login", command=self.login)
        self.loginbtn.grid(row=4, column=1, sticky="nsew", padx=10)

    def login(self):
        """Used for confirming entries are correct"""
        for user in self.master._accounts._accounts:
            if self.accountbox.get() in (user["username"], user["email"]) and user["password"] == self.passwordbox.get():
                self.master.loggedin(user["username"])
                return

        self.feedback.configure(text="Username/email or password is wrong")
        self.feedback.after(3000, lambda:self.feedback.configure(text=""))

    def create_signup_form(self):
        """Used for generating a signup form"""
        for widget in self.winfo_children():
            widget.grid_forget()
        if self.signup_form == None:
            self.signup_form = SignupFrame(self)
            self.signup_form.grid(row=0, column=0, padx=15, pady=15, columnspan=2, rowspan=3, sticky="nsew")


class SignupFrame(ctk.CTkFrame):
    # Frame to create an account
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(9, weight=1)
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
        """Check if all entries are correct"""
        username = self.username_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if any(var == "" for var in (username, age, email, password, confirm_password)):
            self.status_label.configure(text="Please fill in all fields.", text_color="red")
            return

        if "@" in username:
            self.status_label.configure(text="Username cannot contain @", text_color="red")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except:
            self.status_label.configure(text="Please enter a positive whole number for age", text_color="red")
            return

        if not "@" in email:
            self.status_label.configure(text="Email must contain @", text_color="red")
            return

        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match.", text_color="red")
            return

        if username in self.master.master._accounts.get_userdetails("username"):
            self.status_label.configure(text=f"Username {username} is taken.", text_color="red")
            return

        if email in self.master.master._accounts.get_userdetails("email"):
            self.status_label.configure(text="Email already linked to an account.\nIf you would like to create new profiles,\nyou can do so in the profile menu.", text_color="red")
            return

        self.master.master._accounts.add_account(username, age, email, password, "basic")

        self.status_label.configure(text="Account created successfully!", text_color="green")

        self.master.master.newaccountloggedin()

    def cancel_submit(self):
        """Returns to the login screen"""
        self.master.buildui()


class AccountInfoWindow(ctk.CTkToplevel):
    # Frame for showing account information
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title(NAME + " account info")
        #self.relative()
        self.resizable(False, False)
        self.overrideredirect(True)

        self.accountnametxt = ctk.CTkLabel(self, text="Account: "+self.master.master.account)
        self.accountnametxt.grid(row=0, column=0, padx=10, pady=2)

        self.profilenametxt = ctk.CTkLabel(self, text="Profile: "+self.master.master.profile)
        self.profilenametxt.grid(row=1, column=0, padx=10, pady=(0,3))

        self.colorbtn = ctk.CTkButton(self, text="Change Profile Colour", command=self.pick_color)
        self.colorbtn.grid(row=2, column=0, padx=10, pady=3)

        self.subscriptionbtn = ctk.CTkButton(self, text="Subscription", command=self.master.master.maintosubscription)
        self.subscriptionbtn.grid(row=3, column=0, padx=10, pady=3)

        self.profilelist = ctk.CTkComboBox(self, values=self.master.master.profiles)
        self.profilelist.grid(row=4, column=0, padx=10, pady=(30, 3))

        self.switchprofilebtn = ctk.CTkButton(self, text="Switch Profile", command=lambda:self.master.master.switch_profile(self.profilelist.get()))
        self.switchprofilebtn.grid(row=5, column=0, padx=10, pady=3)

        self.logoutbtn = ctk.CTkButton(self, text="Logout", command=master.master.logout)
        self.logoutbtn.grid(row=6, column=0, padx=10, pady=3)

    def relative(self):
        self.update_idletasks()
        self.profilebtn = self.master.profilebtn
        self.geometry(f"160x300+{self.profilebtn.winfo_rootx() - 80}+{self.profilebtn.winfo_rooty() + self.profilebtn.winfo_height() + 10}")

    def updateprofiles(self, profile, profiles:list):
        profiles.remove(profile)
        if profiles:
            self.profilelist.configure(values=profiles) 
            self.profilelist.set(profiles[0])
        else:
            self.profilelist.grid_forget()
            self.switchprofilebtn.grid_forget()

    def pick_color(self):
        self.master.accountinfowindow.withdraw()
        color = ctkcolor.AskColor().get()
        if color:
            self.master.master._accounts.update_color((app:=self.master.master).account, app.profile.name, color)
            self.master.updateprofilebtn()


class BrowseMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.video_images = self.master.load_video_details()

        self.grid_columnconfigure(2, weight=0)

        self.video_list_frame = ctk.CTkScrollableFrame(self, width=650, height=500)
        self.video_list_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)

        self.videomenu = None
        self.video_buttons = []

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=1, column=1, columnspan=10, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.filter_frame, text="Genre").pack(side="top", padx=(5, 2))
        self.genre_filter = ctk.CTkComboBox(self.filter_frame, values=["all", "music", "food", "lifestyle", "education", "adventure", "romance", "horror", "action"])
        self.genre_filter.set("all")
        self.genre_filter.pack(side="top", padx=5)

        ctk.CTkLabel(self.filter_frame, text="Type").pack(side="top", padx=(10, 2))
        self.type_filter = ctk.CTkComboBox(self.filter_frame, values=["all", "user-made video", "short", "TV show", "Movie"])
        self.type_filter.set("all")
        self.type_filter.pack(side="top", padx=5)

        ctk.CTkLabel(self.filter_frame, text="Rating").pack(side="top", padx=(10, 2))
        self.rating_filter = ctk.CTkComboBox(self.filter_frame, values=["all", "G", "PG", "M", "MA", "R"])
        self.rating_filter.set("all")
        self.rating_filter.pack(side="top", padx=5)

        self.back_btn = ctk.CTkButton(self, text="back", command=self.master.browsetomain)
        self.back_btn.grid(row=0, column=0, padx=10, pady=10)

        self.searchbox = ctk.CTkEntry(self, placeholder_text="Search videos...", width=200)
        self.searchbox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.filter_btn = ctk.CTkButton(self, text="Apply Search and Filters", command=self.refresh_videos)
        self.filter_btn.grid(row=1, column=2, padx=10, pady=10, sticky="e")

        self.feedback = ctk.CTkLabel(self, text="No videos found. Try widening your search or filters.")

        self.refresh_videos()

    def refresh_videos(self):
        self.feedback.grid_forget()
        search = self.searchbox.get().lower().strip()

        for widget in self.video_list_frame.winfo_children():
            widget.destroy()

        self.video_buttons.clear()

        genre = self.genre_filter.get()
        content_type = self.type_filter.get()
        rating = self.rating_filter.get()

        row = 2
        for video, info in self.video_images.items():
            if any((genre != "all" and info["genre"] != genre,
                    content_type != "all" and info["type"] != content_type,
                    rating != "all" and info["rating"] != rating,
                    search and search not in video.lower(),
                    self.master.profile.age < 18 and info["rating"] == "R",
                    self.master.profile.age < 15 and info["rating"] in ["R", "MA"])):
                continue

            video_row = ctk.CTkFrame(self.video_list_frame)
            video_row.grid(row=row, column=0, sticky="ew", padx=5, pady=3)

            video_row.grid_columnconfigure(0, weight=1)

            title = ctk.CTkLabel(video_row, text=video, anchor="w")
            title.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

            watchbtn = ctk.CTkButton(video_row, text="Watch", width=100, command=lambda v=video: self.master.open_video(v))
            watchbtn.grid(row=0, column=1, padx=5)

            watchlaterbtn = ctk.CTkButton(video_row, text=("Remove from" if video in self.master.profile.get_wlist() else "Add to") + "\nWatch Later", width=120, command=lambda v=video: self.toggle_watch_later(v))
            watchlaterbtn.grid(row=0, column=2, padx=5)

            row += 1
        if row == 2:
            self.feedback.grid(row=2, column=0, columnspan=3)

    def toggle_watch_later(self, video:str):
        if video in (prof:=self.master.profile).get_wlist():
            prof.remove_from_wlist(video)
        else:
            prof.add_to_wlist(video)
        UserProfiles.save_to_csv(self.master._accounts)
        self.refresh_videos()

    def open_tvshow(self, info, video):
        shows = self.master.load_tvshow_episodes()
        show_name = info["show"]

        episodes = shows[show_name]

        index = next(i for i, ep in enumerate(episodes) if video == ep[1])

        self.master.window = TVEpisodeView(self.master, show_name, episodes, index)


class BaseScrollFrame(ctk.CTkScrollableFrame):
    """Base frame for scrollable frames"""
    def __init__(self, master, string:str="", dir:str="", video=False, **kwargs):
        super().__init__(master, orientation="horizontal"if dir =="x"else"vertical", **kwargs)
        if string:
            ctk.CTkLabel(self, text=string).grid(row=0, column=0, columnspan=100, sticky="w")
        if video: # If frame is used for displaying video buttons
            self.configure(width=650, height=150)
        self.buttons = []

    def add_btn(self, image_path, command=lambda:print(f"No command")):
        if image_path:
            image = ctk.CTkImage(light_image=Image.open(image_path), size=(200, 110))
            btn = ctk.CTkButton(self, command=command, width=200, height=110, image=image, text="", fg_color="transparent", hover_color="#515151")
        else:
            btn = ctk.CTkButton(self, command=command, width=200, height=110, text="No text")
        self.buttons.append(btn)
        btn.grid(row=2, column=len(self.buttons), ipadx=0, ipady=0)

class BaseVideoFrame(ctk.CTkFrame):
    def __init__(self, master, image_path:str, name:str, type:str, backcmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(4, weight=1)
        if not backcmd:
            backcmd = lambda:self.master.videotomain(self)

        self.name = name
        self.image = ctk.CTkLabel(self, text="", image=ctk.CTkImage(light_image=Image.open(image_path), size=(800, 450)))
        self.image.grid(row=0, column=0, rowspan=3, columnspan=2, padx=20, pady=30, sticky="nsew")

        self.textlabel = ctk.CTkLabel(self, text=name, font=("Roboto", 36))
        self.textlabel.grid(row=3, column=0, columnspan=2, pady=10, padx=30, sticky="w")

        self.typelabel = ctk.CTkLabel(self, text=type, font=("Roboto", 36))
        self.typelabel.grid(row=5, column=0, columnspan=2, pady=10, padx=30, sticky="w")

        self.watchbtn = ctk.CTkButton(self, 400, 75, text="Watch", command=lambda:master.open_video(name))
        self.watchbtn.grid(row=0, column=2, columnspan=2, padx=10, pady=5)

        self.watchlaterbtn = ctk.CTkButton(self, 400, 75, text="Add to Watch Later", command=lambda:print("watch_later"))
        self.watchlaterbtn.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

        self.backbtn = ctk.CTkButton(self, 400, 75, text="Back", command=backcmd)
        self.backbtn.grid(row=5, column=2, columnspan=2, padx=5, pady=4)


class TVShowVideoFrame(BaseVideoFrame):
    def __init__(self, master, image_path, name, type, epnumber:int, epbefore:BaseVideoFrame|None, epafter:BaseVideoFrame|None, serieslen:int, backcmd=None, **kwargs):
        super().__init__(master, image_path, name, type, backcmd, **kwargs)
        self.epafter = epafter
        if epnumber != 1:
            ctk.CTkButton(self, text="Previous Episode", command=lambda:print(f"Previous Episode: {epbefore.name}")).grid(row=2, column=2, padx=5, pady=5)
        if epnumber != serieslen:
            ctk.CTkButton(self, text="Next Episode", command=lambda:print(f"Next Episode: {self.epafter.name}")).grid(row=2, column=3, padx=5, pady=5)
        
    def setepafter(self, epafter:BaseVideoFrame):
        self.epafter = epafter


class VideoView(ctk.CTkToplevel, ABC):
    def __init__(self, master, title, image_path, video_type):
        super().__init__(master)

        self.title(title)
        self.geometry("440x440")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1,2), weight=0)

        self.grid_columnconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self, 440, 225)
        self.image = ctk.CTkLabel(self.content,440, 225, text="", image=ctk.CTkImage(light_image=Image.open(image_path), size=(440, 225)))
        self.image.pack()

        self.content.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.back_btn = ctk.CTkButton(self, text="Back", command=self.destroy)

        self.create_navigation()

    @abstractmethod
    def create_navigation(self):
        pass

class TVEpisodeView(VideoView):
    def __init__(self, master, show_name, episodes, start_index=0):
        self.show_name = show_name
        self.episodes = episodes
        self.index = start_index

        super().__init__(master, episodes[self.index][1], episodes[self.index][2]["image"], "TV show")

        self.text = ctk.CTkLabel(self.content, text=f"Episode {episodes[self.index][2]['epnum']}: {episodes[self.index][1]}")
        self.text.pack()

        self.update_buttons()

    def create_navigation(self):
        self.prev_btn = ctk.CTkButton(self, text="Previous Episode", command=self.prev_ep)

        self.next_btn = ctk.CTkButton(self, text="Next Episode", command=self.next_ep)

        self.prev_btn.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.next_btn.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.back_btn.grid(row=2, column=0, columnspan=3, pady=10)

    def load_episode(self):
        ep_info = self.episodes[self.index][2]

        image = ctk.CTkImage(light_image=Image.open(ep_info["image"]), size=(440, 225))

        self.image.configure(image=image)

        self.text.configure(text=f"Episode {self.episodes[self.index][2]['epnum']}: {self.episodes[self.index][1]}")

        if hasattr(self.image, "_resize_needed"):
            self.image.after_cancel(self.image._resize_needed)
            self.image.resize_image()

    def next_ep(self):
        if self.index < len(self.episodes) - 1:
            self.index += 1
            self.load_episode()
            self.update_buttons()

    def prev_ep(self):
        if self.index > 0:
            self.index -= 1
            self.load_episode()
            self.update_buttons()

    def update_buttons(self):
        self.prev_btn.configure(state="normal" if self.index > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.index < len(self.episodes) - 1 else "disabled")


class MovieView(VideoView):
    def __init__(self, master, movie_name, movie_info):
        self.movie_name = movie_name
        self.movie_info = movie_info

        super().__init__(master, movie_name, movie_info["image"], "movie")

    def create_navigation(self):
        self.back_btn.grid(row=1, column=0, pady=10)


class ShortView(VideoView):
    def __init__(self, master, title, info):
        self.info = info

        super().__init__(master, title, info["image"], "short")

    def create_navigation(self):
        self.back_btn.grid(row=1, column=0, pady=10)


class UserMadeView(VideoView):
    def __init__(self, master, title, info):
        self.info = info

        super().__init__(master, title, info["image"], "user-made video")

    def create_navigation(self):
        self.back_btn.grid(row=1, column=0, pady=10)


class MainFrame(ctk.CTkFrame): # better name than mainframe?
    # Frame for after login, watching things idk
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.current_display = None
        self.grid_columnconfigure(10, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.watchlist_setting = master.watchlist_setting

        self.accountinfowindow = AccountInfoWindow(self)
        self.accountinfowindow.withdraw()
        self.subscriptionframe = None

        self.profilebtn = ctk.CTkButton(self, text="", width=60, height=60, corner_radius=30, command=self._open_account_info)
        self.profilebtn.grid(row=0, column=10)

        self.savetocsv = ctk.CTkButton(self, text="save", command=self.savebtn) # dont need anymore?
        self.savetocsv.grid(row=3, column=3)

        self.browsebtn = ctk.CTkButton(self, text="browse", command=self.master.maintobrowse)
        self.browsebtn.grid(row=3, column=4, padx=5)

        self.historybtn = ctk.CTkButton(self, text="watch history", command=self.show_history)
        self.historybtn.grid(row=3, column=5, padx=5)

        self.watchlaterbtn = ctk.CTkButton(self, text="watch later", command=self.show_watch_later)
        self.watchlaterbtn.grid(row=3, column=6, padx=5)

        self.switch = ctk.CTkSwitch(self, text="when watching video, remove from Watch Later", variable=self.watchlist_setting, onvalue=True, offvalue=False)
        self.switch.grid(row=2, column=3, columnspan=3, pady=10)

        self.historyframe = BaseScrollFrame(self, dir="y", width=350, height=250)
        self.historyframe.grid(row=4, column=3, columnspan=4, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.history_widgets = []

        self.scrolls = BaseScrollFrame(self, dir="y")
        self.scrolls.grid(row=6, column=0, columnspan=10, rowspan=2, padx=2, pady=2, sticky="ew")

    def make_accountinfowindow(self):
        self.accountinfowindow = AccountInfoWindow(self)
        self.accountinfowindow.withdraw()

    def updateaccounttxt(self, account, profile):
        self.accountinfowindow.accountnametxt.configure(text="Account: "+account)
        self.accountinfowindow.profilenametxt.configure(text="Profile: "+profile)

    def _open_account_info(self):
        if self.accountinfowindow.state() != "normal":
            self.accountinfowindow.relative()
            self.accountinfowindow.deiconify()
        else:
            self.accountinfowindow.withdraw()

    def update_history_display(self, title, items):
        for widget in self.history_widgets:
            widget.destroy()

        self.history_widgets.clear()

        items = [x for x in items if x]

        if not items:
            label = ctk.CTkLabel(self.historyframe, text=f"No videos in {title}")
            label.grid(row=1, column=0, sticky="w", padx=5)
            self.history_widgets.append(label)
            return

        heading = ctk.CTkLabel(self.historyframe, text=title)
        heading.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 10))

        self.history_widgets.append(heading)

        for row, video in enumerate(items, start=1):
            label = ctk.CTkLabel(self.historyframe, text=video, anchor="w")
            label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

            self.history_widgets.append(label)

    def add_video_to_history(self, video):
        self.master.profile.add_to_whistory(video)
        UserProfiles.save_to_csv(self.master._accounts)

    def show_history(self):
        if self.current_display == "history":
            self.clear_history_display()
            return

        self.current_display = "history"

        history = [v for v in self.master.profile.get_whistory()]
        self.update_history_display("Watch History", history)

    def show_watch_later(self):
        if self.current_display == "watchlater":
            self.clear_history_display()
            return

        self.current_display = "watchlater"

        wlist = [v for v in self.master.profile.get_wlist()]
        self.update_history_display("Watch Later", wlist)

    def clear_history_display(self):
        for widget in self.history_widgets:
            widget.destroy()

        self.history_widgets.clear()
        self.current_display = None

    def savebtn(self):
        self.master._accounts.save_to_csv()
        UserProfiles.save_to_csv(self.master._accounts)

    def _darken_color(self, color, amount): # amount is a % of the rgb value to reduce
        c = color[1:]
        r = round(int(c[0:2], 16) * (1-amount/100))
        g = round(int(c[2:4], 16) * (1-amount/100))
        b = round(int(c[4:6], 16) * (1-amount/100))
        return f"#{r:02x}{g:02x}{b:02x}"

    def updateprofilebtn(self):
        self.profilebtn.configure(text=self.master.profile.name[0], fg_color=self.master.profile.color, hover_color=self._darken_color(self.master.profile.color, 20))



class SubscriptionFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.form_frame = BaseScrollFrame(self, dir="y", height=500, width=650)

        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        account = self.master.account
        current_plan = self.master._accounts.get_subscription(account)

        ctk.CTkLabel(self.form_frame, text=f"Current Plan: {current_plan}").pack(pady=(10,0))

        ctk.CTkLabel(self.form_frame, text="Available plans: basic (free), premium ($5/month), 神様 ($67/month)").pack(pady=(10,0))

        ctk.CTkLabel(self.form_frame, text="Input fields have been pre-filled with known information, if any.\nRemember to change if details have changed.\n-----------------").pack(pady=(10,5))

        ctk.CTkLabel(self.form_frame, text="Subscription").pack()
        self.form_frame.planbox = ctk.CTkComboBox(self.form_frame, values=["basic", "premium", "神様"])
        self.form_frame.planbox.pack(pady=(0,5))

        # label text, placeholder text, hidden with asterisk?
        fields = {"cardholder": ("Cardholder Name", "e.g. Ryan Dunne", False, 200),
                  "cardnumber": ("Card Number", "e.g. https://en.wikipedia.org/wiki/Luhn_algorithm", False, 200),
                  "expiry": ("Expiration Date (MM/YY)", "e.g. 01/67", False, 200),
                  "security": ("Security Code", "e.g. 420", True, 200),
                  "billing": ("Billing Address", "e.g. 419A Windsor Road", False, 300)}
        self.subscription_entries = {}

        for key, (label_text, placeholder, hidden, width) in fields.items():
            ctk.CTkLabel(self.form_frame, text=label_text).pack(pady=(5, 0))

            entry = ctk.CTkEntry(self.form_frame, placeholder_text=placeholder, show="*" if hidden else "", width=width)
            entry.pack(pady=(0,5))

            self.subscription_entries[key] = entry

        self.successlabel = ctk.CTkLabel(self, text="")
        self.successlabel.grid(row=1, column=0, pady=5)

        acc = self.master._accounts.get_account(self.master.account)
        self.set_entry(self.subscription_entries["cardholder"], acc.get("cardholder", ""))
        self.set_entry(self.subscription_entries["cardnumber"], acc.get("cardnumber", ""))
        self.set_entry(self.subscription_entries["expiry"], acc.get("expiry", ""))
        self.set_entry(self.subscription_entries["security"], acc.get("securitycode", ""))
        self.set_entry(self.subscription_entries["billing"], acc.get("billingaddress", ""))

        ctk.CTkButton(self, text="Update Subscription", command=self.update_subscription).grid(row=2, column=0, pady=5)

        ctk.CTkButton(self, text="Back", command=self.master.subscriptiontomain).grid(row=3, column=0, pady=5)

    def set_entry(self, entry, value):
        if value:
            entry.insert(0, value)

    def luhn_verify(self, number): # verifies that number follows Luhn algorithm, returns passed (bool), error (str)
        if not number.isdigit():
            return False, "Please enter only digits (no punctuation) for the card number."

        runningtotal = 0
        payload = list(number[-2::-1])
        for i in range(len(payload)):
            currentterm = int(payload[i]) * (2 - i % 2)
            if currentterm > 9:
                currentterm -= 9
            runningtotal += currentterm

        if int(number[-1]) != (10 - (runningtotal % 10)) % 10:
            return False, "Error: checksum incorrect. Please make sure you have typed your card number correctly."

        return True, ""

    def date_verify(self, date): # verifies that date is a real date (MM/YY) and is not expired, returns passed (bool), error (str)
        try:
            month, year = date.split("/")
            month = int(month)
            year = 2000 + int(year)

            if not 2000 <= year <= 2099:
                return False, "Error: expiry year is invalid"

            if not 1 <= month <= 12:
                return False, "Error: expiry month is invalid"

            if (year, month) < (datetime.now().year, datetime.now().month):
                return False, "Error: card is expired"

            return True, ""

        except ValueError:
            return False, "Error: expiry date is not in MM/YY format"

    def update_subscription(self):
        prices = {"basic": 0, "premium": 5, "神様": 67}
        details = (self.subscription_entries["cardholder"].get(),
                   self.subscription_entries["cardnumber"].get(),
                   self.subscription_entries["expiry"].get(),
                   self.subscription_entries["security"].get(),
                   self.subscription_entries["billing"].get())

        if not all(details):
            self.successlabel.configure(text="Please fill in all fields.", text_color="red")
            return

        passed_luhn, error = self.luhn_verify(details[1])
        if not passed_luhn:
            self.successlabel.configure(text=error, text_color="red")
            return

        passed_date, error = self.date_verify(details[2])
        if not passed_date:
            self.successlabel.configure(text=error, text_color="red")
            return

        if not details[3].isdigit():
            self.successlabel.configure(text="Error: security code must be a number.", text_color="red")
            return

        self.master._accounts.update_subscription(self.master.account, self.form_frame.planbox.get(), *details)

        with open(f"{self.master.account}_invoice.txt", "w", encoding="utf-8") as f:
            f.write(f"i love {NAME}, you love {NAME}, we love {NAME} streaming service :3\n\n")

            f.write("--------------------\n")
            f.write("SUBSCRIPTION INVOICE\n")
            f.write("--------------------\n\n")

            f.write(f"Account Name: {self.master.account}\n")
            f.write(f"Plan: {self.form_frame.planbox.get()} (${str(prices[self.form_frame.planbox.get()])}/month)\n")
            f.write(f'Cardholder: {details[0]}\n')
            f.write(f'Billing Address: {details[4]}\n\n')

            f.write("---------------\n")
            f.write("VIEWING HISTORY\n")
            f.write("---------------\n")

            history = self.master.profile.get_whistory()

            if history:
                for video in history:
                    f.write(f"- {video}\n")
            else:
                f.write("No viewing history.\n")

        self.successlabel.configure(text="Subscription updated successfully!", text_color="green")


class StreamingServiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(NAME + " streaming service :3 ")
        self.WIDTH = 720
        self.HEIGHT = 1080
        self.X = 100
        self.Y = 100
        self.resizable(False, False)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X}+{self.Y}")

        self.watchlist_setting = ctk.BooleanVar(value=False)
        self.videos:dict[list[dict]] = {} # {showtype: [{class:class, moreinfo: info}], showtype: [{}]}
        # eg. {tvshow: [{class:class, show:showname, epnum:1}]}

        self.window = None

        self._accounts = UserAccounts()
        self._accounts.load_from_csv()
        self.account = ""
        self.profiles = self._accounts.get_profiles(self.account)
        self.profile = ""
        UserProfiles.load_from_csv(self._accounts)

        self.logo = ctk.CTkImage(light_image=Image.open("logo.png"), size=(40, 40))
        ctk.CTkLabel(self, text=" "+NAME, text_color="pink", image=self.logo, compound="left").pack(side="top", pady=(10, 10))

        self.login = LoginFrame(self)
        self.login.pack(fill="both", expand=True, padx=40, pady=(10, 20))

        self.main = MainFrame(self)

    def loggedin(self, username):
        self.changeframetomain()
        self.account = username
        self.loginupdate(self.account)

    def newaccountloggedin(self):
        self.changeframetomain()
        self.account = self.login.signup_form.username_entry.get()
        self.loginupdate(self.account)

    def loginupdate(self, username):
        self.profile = self._accounts.get_profiles(self.account)[0]
        self.main.updateaccounttxt(self.account, (pname:=self.profile.name))
        self.main.accountinfowindow.updateprofiles(pname, self._accounts.get_profilesnames(username))
        self.main.updateprofilebtn()
        self.update_profiles()
        self.browsemenu = BrowseMenu(self)
        self.subscription = SubscriptionFrame(self)
        self.generate_scroll("food")
        self.generate_scroll(video_type="usermade")
        self.load_tvshows()

    def update_profiles(self):
        self.profiles = self._accounts.get_profiles(self.account)

    def switch_profile(self, profile:str):
        for i, p in enumerate(map(lambda p:p.name,self._accounts.get_profiles(self.account))):
            if p == profile:
                self.profile = self.profiles[i]
                self.main.updateaccounttxt(self.account, self.profile.name)
                self.main.updateprofilebtn()
                self.main.accountinfowindow.updateprofiles(self.profile.name, self._accounts.get_profilesnames(self.account))
                self.main.clear_history_display()
                self.browsemenu.refresh_videos()
                break

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
        self.main.clear_history_display()
        self.main.accountinfowindow.withdraw()

    def maintobrowse(self):
        self.main.clear_history_display()
        self.main.accountinfowindow.withdraw()
        self.main.forget()
        self.browsemenu.pack(fill="both", expand=True)
        self.browsemenu.refresh_videos()

    def browsetomain(self):
        self.browsemenu.forget()
        self.browsemenu.feedback.grid_forget()
        self.browsemenu.searchbox.delete(0, "end")
        self.browsemenu.type_filter.set("all")
        self.browsemenu.genre_filter.set("all")
        self.browsemenu.rating_filter.set("all")
        self.main.pack(fill="both", expand=True)

    def maintosubscription(self):
        self.main.clear_history_display()
        self.main.accountinfowindow.withdraw()
        self.main.forget()
        self.subscription.pack(fill="both", expand=True)

    def subscriptiontomain(self):
        self.subscription.forget()
        self.main.pack(fill="both", expand=True)

    def videotomain(self, videoframe:BaseVideoFrame):
        videoframe.forget()
        self.main.pack(fill="both", expand=True)

    def maintovideo(self, videoframe:BaseVideoFrame):
        self.main.forget()
        videoframe.pack(fill="both", expand=True)

    def load_video_details(self, type:str="all") -> dict[dict]:
        videos:dict[dict] = {}
        if type == "all" or type == "short":
            with open("video_details/short_details.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    videos[row["title"]] = {"image": "video_images/" + row["image"],
                                            "genre": row["genre"],
                                            "type": "short",
                                            "user": row["user"],
                                            "rating": row["rating"]}
        if type == "all" or type == "tvshow":
            with open("video_details/tvshow_details.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    videos[row["title"]] = {"image": "video_images/" + row["image"],
                                            "genre": row["genre"],
                                            "type": "TV show",
                                            "rating": row["rating"],
                                            "show": row["show"],
                                            "epnum": int(row["episodenum"])}
        if type == "all" or type == "usermade":
            with open("video_details/usermade_details.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    videos[row["title"]] = {"image": "video_images/" + row["image"],
                                            "genre": row["genre"],
                                            "type": "user-made video",
                                            "rating": row["rating"],
                                            "user": row["user"]}
        if type == "all" or type == "movie":
            with open("video_details/movie_details.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    videos[row["title"]] = {"image": "video_images/" + row["image"],
                                            "genre": row["genre"],
                                            "type": "Movie",
                                            "director": row["director"],
                                            "rating": row["rating"]}
        return videos

    def open_video(self, video:str):
        if self.window and self.window.winfo_exists():
            self.window.destroy()
      
        self.main.add_video_to_history(video)

        if self.watchlist_setting.get():
            self.profile.remove_from_wlist(video)
            self.main.refresh_videos()

        info = self.browsemenu.video_images[video]

        if info["type"] == "TV show":
            self.browsemenu.open_tvshow(info, video)
            return
          
        if info["type"] == "Movie":
            self.window = MovieView(self.master, video, info)
            return

        
        if info["type"] == "short":
            self.window = ShortView(self.master, video, info)
            return

        if info["type"] == "user-made video":
            self.window = UserMadeView(self.master, video, info)
            return

        else:
            self.window.destroy()

    def load_tvshows(self):
        shows = self.load_tvshow_episodes()
        for show, eps in shows.items():
            scroll = BaseScrollFrame(self.main.scrolls, show, "x", True)
            scroll.pack()
            for id, ep, details in eps:
                showframe = BaseVideoFrame(self, details["image"], ep, "tvshow")
                scroll.add_btn(details["image"], lambda:self.maintovideo(showframe))
            

    def generate_scroll(self, genre:str="", video_type:str="", rating:str=""):
        """
        Generates a scroll frame with the window buttons based on the filters\n
        genre: food, music, education, lifestyle, None(default -> all)\n
        video_type: usermade, short, None(default -> all)\n
        rating: G, PG, M, MA, R, None(default -> all)
        """
        typetxt = {"usermade": "user-made videos", "short": "shorts", "": "videos"}
        string = f"{rating}{' rated ' if rating else ''}{genre} {typetxt[video_type]}"       
        scroll = BaseScrollFrame(self.main.scrolls, string, "x", True)
        scroll.pack()
        if not genre and not video_type and not rating:
            return
        if video_type:
            videos = self.load_video_details(video_type)
        else:
            videos = self.load_video_details("usermade") | self.load_video_details("short")

        for video, details in videos.items():
            if any((genre and details["genre"] != genre,
                    rating and details["rating"] != rating,
                    self.profile.age < 18 and details["rating"] == "R",
                    self.profile.age < 15 and details["rating"] in ["R", "MA"])):
                continue

            frame = BaseVideoFrame(self, details["image"], video, details["type"])

            scroll.add_btn(details["image"], command=lambda f=frame: self.maintovideo(f))

    def load_tvshow_episodes(self):
        episodes = self.load_video_details("tvshow")

        shows:dict[list[tuple]] = {}
        for title, info in episodes.items():
            show = info["show"]
            if not show in shows:
                shows[show] = []
            shows[show].append((info["epnum"], title, info))

        for show in shows:
            shows[show].sort(key=lambda x: x[0])

        return shows


class UserAccounts:
    # Only handles data
    FIELDS = ["username", "age", "email", "password", "profiles", "subscription", "cardholder", "cardnumber", "expiry", "securitycode", "billingaddress", "rgb"]
    filepath = "accounts.csv"

    def __init__(self):
        self._accounts:list[dict] = []
        self._profiles:dict[list] = {}

    def add_account(self, username, age, email, password, subscription="basic"):
        self._accounts.append({"username": username,
                               "age": age,
                               "email": email,
                               "password": password,
                               "profiles": f"{username}:{age}",
                               "subscription": subscription,
                               "cardholder": "",
                               "cardnumber": "",
                               "expiry": "",
                               "securitycode": "",
                               "billingaddress": "",
                               "rgb": ""})
        self._profiles[username] = [UserProfiles(username, age)]

    def get_account(self, username) -> dict|None:
        for account in self._accounts:
            if account["username"] == username:
                return account
        return None

    def get_userdetails(self, detail) -> list:
        return [*map(lambda user: user[detail], self._accounts)]

    def get_profiles(self, username) -> list:
        try:
            return self._profiles[username]
        except:
            return []

    def get_profile_dict(self) -> dict:
        return self._profiles

    def get_profilesnames(self, username:str) -> list:
        return [*map(lambda profile:profile.name, self._profiles[username])]

    def get_all(self) -> list:
        return list(self._accounts)

    def save_to_csv(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(self._accounts)

    def load_from_csv(self):
        colors:dict[list[str]] = {}
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._accounts.append({"username": row["username"],
                                       "age": row["age"],
                                       "email": row["email"],
                                       "password": row["password"],
                                       "profiles": row["profiles"],
                                       "subscription": row["subscription"],
                                       "cardholder": row.get("cardholder", ""),
                                       "cardnumber": row.get("cardnumber", ""),
                                       "expiry": row.get("expiry", ""),
                                       "securitycode": row.get("securitycode", ""),
                                       "billingaddress": row.get("billingaddress", ""),
                                       "rgb": row["rgb"]})
                self._profiles[row["username"]] = []
                if row["profiles"]:
                    for profile in row["profiles"].split(";"):
                        # profile should be name:age;name:age
                        self._profiles[row["username"]].append(UserProfiles((plist:=profile.split(":"))[0], int(plist[1]), [], []))
                colors[row["username"]] = row["rgb"].split(":")
        self.update_color_all(colors)

    def get_subscription(self, username:str) -> str:
        for account in self._accounts:
            if account["username"] == username:
                return account["subscription"]

    def update_subscription(self, username, subscription, cardholder, cardnumber, expiry, securitycode, billingaddress):
        for account in self._accounts:
            if account["username"] == username:
                account["subscription"] = subscription
                account["cardholder"] = cardholder
                account["cardnumber"] = cardnumber
                account["expiry"] = expiry
                account["securitycode"] = securitycode
                account["billingaddress"] = billingaddress
                break
        self.save_to_csv()

    def update_color(self, username:str, name:str, rgb):
        (profiles:=self._profiles[username])[self.get_profilesnames(username).index(name)].color = rgb
        colors = []
        for p in profiles:
            colors.append(p.color)
        colortxt = ":".join(colors)
        self._accounts[self.get_userdetails("username").index(username)]["rgb"] = colortxt

    def update_color_all(self, colors:dict[list[str]]):
        for username in [*self._profiles.keys()]:
            profile_colors = colors[username]
            for i, profile in enumerate(self._profiles[username]):
                self.update_color(username, profile.name, profile_colors[i])


class UserProfiles():

    FIELDS = ["name", "wlist", "whistory"]

    def __init__(self, name:str, age:int, wlist:list, whistory:list, color=None):
        self.name = name
        self.age = age
        self._watch_list = wlist
        self._watch_history = whistory
        self.color = color or ctk.ThemeManager.theme["CTkButton"]["fg_color"][int(ctk.get_appearance_mode() == "Dark")]

    def load_from_csv(account:UserAccounts):
        with open("profiles.csv", "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            profiles = account.get_profile_dict()
            for row in reader:
                name = row["name"]
                profiles_watch_list = row["wlist"].split(";67;")
                profile_watch_history = row["whistory"].split(";67;")
                for i in range(len(profiles_watch_list)):
                    profile = profiles[name][i]
                    watch_list = profiles_watch_list[i].split("|67|") # watch list in the profile in the account
                    watch_history = profile_watch_history[i].split("|67|")
                    for video in watch_list:
                        profile.add_to_wlist(video)
                    for video in watch_history:
                        profile.add_to_whistory(video)

    def save_to_csv(account:UserAccounts):
        # Change UserProfiles class into a dict
        profiles = account.get_profile_dict()
        # {name: [UserProfiles(), UserProfiles()], name: [UserProfiles()]}
        plist = []
        # ;67; separates the profiles
        # |67| separates the wlist and whistory items
        # becomes:
        # name, video1|video2|video3;video2|video1, video4;video3|video4
        for i in range(len(profiles)):
            wlist = []
            whistorylist = []
            for profile in [*profiles.values()][i]:
                wlist.append(wl if (wl:="|67|".join(profile._watch_list))[:4] != "|67|" else wl[4:])
                whistorylist.append(wh if (wh:="|67|".join(profile._watch_history))[:4] != "|67|" else wh[4:])
            wlisttxt = ";67;".join(wlist)
            whistorytxt = ";67;".join(whistorylist)
            plist.append({"name":[*profiles.keys()][i], "wlist":wlisttxt, "whistory":whistorytxt})           
        with open("profiles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "wlist", "whistory"])
            writer.writeheader()
            writer.writerows(plist)

    def add_to_whistory(self, id:str):
        self.remove_from_whistory(id)
        self._watch_history.append(id)

    def remove_from_whistory(self, id:str):
        if id in self._watch_history:
            self._watch_history.remove(id)

    def get_whistory(self) -> list:
        return self._watch_history

    def add_to_wlist(self, id:str):
        self.remove_from_wlist(id)
        self._watch_list.append(id)

    def remove_from_wlist(self, id:str):
        if id in self._watch_list:
            self._watch_list.remove(id)

    def get_wlist(self) -> list:
        return self._watch_list


app = StreamingServiceApp()
app.after(0, lambda: app.state("zoomed"))
app.mainloop()