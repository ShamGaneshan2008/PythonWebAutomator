import tkinter as tk
from tkinter import messagebox
import threading
from main import WebAutomation


BG = "#0f1117"
PANEL = "#1a1d27"
BORDER = "#2a2d3e"
ACCENT = "#4f8ef7"
SUCCESS = "#3ecf8e"
ERROR = "#f76f6f"
WARN = "#f7c44f"
FG = "#e8eaf0"
MUTED = "#6b7280"
ENTRY_BG = "#12151f"

FONT_BODY = ("Consolas", 10)
FONT_LABEL = ("Consolas", 9)
FONT_TITLE = ("Georgia", 15, "bold")
FONT_BTN = ("Consolas", 10, "bold")


# Helper Widgets
def make_entry(parent, show=None):
    return tk.Entry(
        parent,
        font=FONT_BODY,
        bg=ENTRY_BG,
        fg=FG,
        insertbackground=ACCENT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        show=show
    )


def make_label(parent, text):
    return tk.Label(parent, text=text, font=FONT_LABEL, bg=PANEL, fg=FG)


def make_button(parent, text, command, color):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BTN,
        bg=color,
        fg=BG,
        relief="flat",
        cursor="hand2",
        pady=8
    )

    btn.bind("<Enter>", lambda e: btn.config(bg=FG))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))

    return btn


# Main App
class App:

    def __init__(self, root):
        self.root = root
        self.bot = None

        self.root.title("Web Automation")
        self.root.configure(bg=BG)
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.build_ui()


    # UI Layout
    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Web Automation Bot",
            font=FONT_TITLE,
            bg=BG,
            fg=ACCENT
        )

        title.pack(pady=20)

        frame = tk.Frame(self.root, bg=PANEL, padx=20, pady=20)
        frame.pack(padx=20, fill="x")

        make_label(frame, "Username").pack(anchor="w")
        self.entry_username = make_entry(frame)
        self.entry_username.pack(fill="x", pady=5)

        make_label(frame, "Password").pack(anchor="w")
        self.entry_password = make_entry(frame, show="*")
        self.entry_password.pack(fill="x", pady=5)

        make_label(frame, "Full Name").pack(anchor="w")
        self.entry_fullname = make_entry(frame)
        self.entry_fullname.pack(fill="x", pady=5)

        make_label(frame, "Email").pack(anchor="w")
        self.entry_email = make_entry(frame)
        self.entry_email.pack(fill="x", pady=5)

        make_label(frame, "Current Address").pack(anchor="w")
        self.entry_current = make_entry(frame)
        self.entry_current.pack(fill="x", pady=5)

        make_label(frame, "Permanent Address").pack(anchor="w")
        self.entry_permanent = make_entry(frame)
        self.entry_permanent.pack(fill="x", pady=5)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=20)

        make_button(btn_frame, "Submit Form", self.submit_thread, ACCENT).pack(side="left", padx=5)

        make_button(btn_frame, "Download File", self.download_thread, "#6c63ff").pack(side="left", padx=5)

        make_button(btn_frame, "Close Browser", self.close_browser, "#2a2d3e").pack(side="left", padx=5)

        # Log box
        self.log = tk.Text(
            self.root,
            height=10,
            bg=ENTRY_BG,
            fg=FG,
            font=("Consolas", 9),
            state="disabled"
        )

        self.log.pack(fill="x", padx=20, pady=10)

        self.write_log("Application ready")


    # Logging
    def write_log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")


    # Submit Form
    def submit_thread(self):
        threading.Thread(target=self.submit_form, daemon=True).start()

    def submit_form(self):

        username = self.entry_username.get()
        password = self.entry_password.get()
        fullname = self.entry_fullname.get()
        email = self.entry_email.get()
        current = self.entry_current.get()
        permanent = self.entry_permanent.get()

        if not username or not password:
            self.write_log("Username or password missing")
            return

        try:

            self.bot = WebAutomation()

            self.bot.start_browser()
            self.bot.login(username, password)
            self.bot.fill_form(fullname, email, current, permanent)

            self.write_log("Form submitted successfully")

            messagebox.showinfo("Success", "Form submitted successfully!")

        except Exception as e:

            self.write_log(str(e))
            messagebox.showerror("Error", str(e))


    # Download
    def download_thread(self):
        threading.Thread(target=self.download, daemon=True).start()

    def download(self):

        if not self.bot:
            self.write_log("No browser session active")
            return

        try:

            self.bot.download()
            self.write_log("Download started")

        except Exception as e:
            self.write_log(str(e))


    # Close Browser
    def close_browser(self):

        if self.bot:
            self.bot.close()
            self.bot = None
            self.write_log("Browser closed")
        else:
            self.write_log("No browser to close")



# Run GUI
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()