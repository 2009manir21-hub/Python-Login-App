import tkinter as tk
from tkinter import messagebox
import csv
import os
import sys

# --------------------------------------------------

windo = tk.Tk()
windo.title("Sign in")
LOGO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_logo.png")
try:
    app_logo = tk.PhotoImage(file=LOGO_FILE)
    windo.iconphoto(True, app_logo)
except (tk.TclError, OSError):
    app_logo = None 
windo.geometry("400x400")
windo.config(bg="black")
windo.resizable(0, 0)
page_frame = tk.Frame(windo, bg="black")
page_frame.pack(fill="both", expand=True)

# --------------------------------------------------

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(APP_DIR, "login_data.csv")
def ensure_csv_file():
    folder = os.path.dirname(CSV_FILE)
    try:
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(CSV_FILE, "x", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password"])
            writer.writeheader()
    except FileExistsError:
        pass
    except (PermissionError, OSError) as error:
        messagebox.showerror(
            "Error",
            f"Cannot create CSV file:\n{error}",
            parent=windo
        )
current_username = ""
current_page = 0
user_index = 0
def clear_page():
    for widget in page_frame.winfo_children():
        widget.destroy()

#  --------------------------------------------------

def read_users():
    users = []
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "username" in row and "password" in row:
                    users.append(row)
    except FileNotFoundError:
        folder = os.path.dirname(CSV_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["username", "password"]
            )
            writer.writeheader()
    except (PermissionError, OSError) as error:
        messagebox.showerror(
            "Error",
            f"Cannot read CSV file:\n{error}",
            parent=windo
        )
    return users

# --------------------------------------------------

def save_users(users):
    try:
        folder = os.path.dirname(CSV_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["username", "password"]
            )
            writer.writeheader()
            writer.writerows(users)
        return True
    except (PermissionError, OSError) as error:
        messagebox.showerror(
            "Error",
            f"Could not save data:\n{error}",
            parent=windo
        )
        return False

# --------------------------------------------------

def sign_in():
    global current_username
    username = entry_username.get().strip()
    password = entry_password.get()
    if username == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please enter username and password",
            parent=windo
        )
        return
    users = read_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            current_username = username
            open_page()
            return
    messagebox.showerror(
        "Error",
        "Wrong username or password",
        parent=windo
    )

# --------------------------------------------------

def sign_up():
    clear_page()
    windo.title("Sign Up")
    def register_user():
        username = entry_signup_username.get().strip()
        password = entry_signup_password.get()
        repeat_password = entry_repeat_password.get()
        if not username or not password or not repeat_password:
            messagebox.showerror(
                "Error",
                "Please fill in all fields",
                parent=windo
            )
            return
        if password != repeat_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match",
                parent=windo
            )
            return
        users = read_users()
        for user in users:
            if user["username"] == username:
                messagebox.showerror(
                    "Error",
                    "This username already exists",
                    parent=windo
                )
                return
        users.append({
            "username": username,
            "password": password
        })
        if save_users(users):
            messagebox.showinfo(
                "Success",
                "Registration was successful",
                parent=windo
            )
            show_login()

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="Sign Up",
        font=("Bahnschrift", 30, "bold"),
        bg="black",
        fg="white"
    ).place(x=130, y=30)
    tk.Label(
        page_frame,
        text="username",
        font=("Bahnschrift", 12),
        bg="black",
        fg="white"
    ).place(x=25, y=110)
    entry_signup_username = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white"
    )
    entry_signup_username.place(x=125, y=113)

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="password",
        font=("Bahnschrift", 12),
        bg="black",
        fg="white"
    ).place(x=27, y=160)
    entry_signup_password = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white",
        show="*"
    )
    entry_signup_password.place(x=125, y=163)

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="repeat password",
        font=("Bahnschrift", 10),
        bg="black",
        fg="white"
    ).place(x=15, y=210)
    entry_repeat_password = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white",
        show="*"
    )
    entry_repeat_password.place(x=125, y=213)

    # --------------------------------------------------

    tk.Button(
        page_frame,
        text="Register",
        font=("Bahnschrift", 13),
        bd=0,
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=register_user
    ).place(x=155, y=260)
    tk.Button(
        page_frame,
        text="Back",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="gray",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=show_login
    ).place(x=175, y=300)

# --------------------------------------------------

def change_information():
    global current_username
    new_username = entry_new_username.get().strip()
    new_password = entry_new_password.get()
    repeat_password = entry_change_repeat_password.get()
    if not new_username or not new_password or not repeat_password:
        messagebox.showerror(
            "Error",
            "Please fill in all fields",
            parent=windo
        )
        return
    if new_password != repeat_password:
        messagebox.showerror(
            "Error",
            "Passwords do not match",
            parent=windo
        )
        return
    users = read_users()
    for user in users:
        if user["username"] == new_username and new_username != current_username:
            messagebox.showerror(
                "Error",
                "This username already exists",
                parent=windo
            )
            return
    for user in users:
        if user["username"] == current_username:
            user["username"] = new_username
            user["password"] = new_password
            if save_users(users):
                current_username = new_username
                messagebox.showinfo(
                    "Success",
                    "Your information was changed",
                    parent=windo
                )
                open_page()
            return
    messagebox.showerror(
        "Error",
        "User not found",
        parent=windo
    )

# --------------------------------------------------

def open_change_window():
    clear_page()
    windo.title("Change Information")

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="Change Information",
        font=("Bahnschrift", 22, "bold"),
        bg="black",
        fg="white"
    ).place(x=65, y=35)

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="new username",
        font=("Bahnschrift", 10),
        bg="black",
        fg="white"
    ).place(x=25, y=115)

    global entry_new_username, entry_new_password, entry_change_repeat_password

    entry_new_username = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white"
    )
    entry_new_username.place(x=145, y=118)
    entry_new_username.insert(0, current_username)

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="new password",
        font=("Bahnschrift", 10),
        bg="black",
        fg="white"
    ).place(x=25, y=165)

    entry_new_password = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white",
        show="*"
    )
    entry_new_password.place(x=145, y=168)

    # --------------------------------------------------

    tk.Label(
        page_frame,
        text="repeat password",
        font=("Bahnschrift", 10),
        bg="black",
        fg="white"
    ).place(x=25, y=215)

    entry_change_repeat_password = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white",
        show="*"
    )
    entry_change_repeat_password.place(x=145, y=218)

    # --------------------------------------------------

    tk.Button(
        page_frame,
        text="Save Changes",
        font=("Bahnschrift", 11),
        bd=0,
        bg="black",
        fg="gray",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=change_information
    ).place(x=145, y=280)

    tk.Button(
        page_frame,
        text="Back",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="gray",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=open_page
    ).place(x=175, y=320)

# --------------------------------------------------

def open_page():
    global current_page, user_index

    clear_page()
    windo.title(current_username)

    users = read_users()
    if not users:
        show_login()
        return

    user_index = 0
    for index, user in enumerate(users):
        if user["username"] == current_username:
            user_index = index
            break

    # --------------------------------------------------

    label_username_title = tk.Label(
        page_frame,
        text="Username",
        font=("Bahnschrift", 12),
        bg="black",
        fg="gray"
    )
    label_username_title.place(x=160, y=45)

    label_display_username = tk.Label(
        page_frame,
        text="",
        font=("Bahnschrift", 20, "bold"),
        bg="black",
        fg="white"
    )
    label_display_username.place(x=(400 - label_display_username.winfo_reqwidth()) // 2, y=75)

    # --------------------------------------------------

    label_password_title = tk.Label(
        page_frame,
        text="Password",
        font=("Bahnschrift", 12),
        bg="black",
        fg="gray"
    )
    label_password_title.place(x=160, y=125)

    label_display_password = tk.Label(
        page_frame,
        text="",
        font=("Bahnschrift", 12),
        bg="black",
        fg="white"
    )
    label_display_password.place(x=(400 - label_display_password.winfo_reqwidth()) // 2, y=155)

    # --------------------------------------------------

    btn_change = tk.Button(
        page_frame,
        text="Change Username / Password",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="gray",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=open_change_window
    )
    btn_change.place(x=105, y=205)

    label_page = tk.Label(
        page_frame,
        text="",
        font=("Bahnschrift", 10),
        bg="black",
        fg="gray"
    )
    label_page.place(x=155, y=290)

    # --------------------------------------------------

    def display_user(index):
        global user_index, current_page

        users_now = read_users()
        if not users_now:
            label_display_username.config(text="")
            label_display_password.config(text="")
            label_password_title.place_forget()
            btn_change.place_forget()
            label_page.config(text="No users")
            return

        index = max(0, min(index, len(users_now) - 1))
        user_index = index
        selected_user = users_now[index]

        label_display_username.config(text=selected_user["username"])
        label_display_username.place(x=(400 - label_display_username.winfo_reqwidth()) // 2, y=75)
        windo.title(selected_user["username"])

        if selected_user["username"] == current_username:
            label_password_title.place(x=155, y=125)
            label_display_password.config(text=selected_user["password"])
            label_display_password.place(x=(400 - label_display_password.winfo_reqwidth()) // 2, y=155)
            btn_change.place(x=105, y=205)
        else:
            label_password_title.place_forget()
            label_display_password.config(text="")
            label_display_password.place_forget()
            btn_change.place_forget()

        current_page = index
        label_page.config(text=f"User {index + 1} / {len(users_now)}")
        btn_previous.config(state="normal" if index > 0 else "disabled")
        btn_next.config(state="normal" if index < len(users_now) - 1 else "disabled")

    # --------------------------------------------------

    def previous_user():
        display_user(user_index - 1)

    def next_user():
        display_user(user_index + 1)

    # --------------------------------------------------

    btn_previous = tk.Button(
        page_frame,
        text="Previous",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=previous_user
    )
    btn_previous.place(x=60, y=330)

    btn_next = tk.Button(
        page_frame,
        text="Next",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=next_user
    )
    btn_next.place(x=290, y=330)

    display_user(user_index)

# --------------------------------------------------

def show_login():
    clear_page()
    windo.title("Sign in")

    label_sign_in = tk.Label(
        page_frame,
        text="Sign in",
        font=("Bahnschrift", 30, "bold"),
        bg="black",
        fg="white"
    )
    label_sign_in.place(x=140, y=60)

    label_info = tk.Label(
        page_frame,
        text="Enter your information to sign in",
        font=("Bahnschrift", 10),
        bg="black",
        fg="gray"
    )
    label_info.place(x=110, y=115)

    label_username = tk.Label(
        page_frame,
        text="username",
        font=("Bahnschrift", 12),
        bg="black",
        fg="white"
    )
    label_username.place(x=25, y=163)

    global entry_username, entry_password

    entry_username = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white"
    )
    entry_username.place(x=115, y=167)

    label_password = tk.Label(
        page_frame,
        text="password",
        font=("Bahnschrift", 12),
        bg="black",
        fg="white"
    )
    label_password.place(x=27, y=213)

    entry_password = tk.Entry(
        page_frame,
        width=30,
        selectbackground="black",
        selectforeground="white",
        show="*"
    )
    entry_password.place(x=115, y=217)

    # --------------------------------------------------

    tk.Button(
        page_frame,
        text="Login",
        font=("Bahnschrift", 13),
        bd=0,
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=sign_in
    ).place(x=173, y=255)

    tk.Button(
        page_frame,
        text="Sign Up",
        font=("Bahnschrift", 10),
        bd=0,
        bg="black",
        fg="gray",
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        command=sign_up
    ).place(x=173, y=290)

# --------------------------------------------------

ensure_csv_file()
show_login()
windo.mainloop()
