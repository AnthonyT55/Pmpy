import customtkinter as ctk

class States:
    def __init__(self, window):
        self.window = window
        self.window.title("PASSMAN")
        self.window.geometry("500x500")
        self.window.resizable(width=True, height=True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.auth_ui()

    def auth_ui(self):
        self.content = ctk.CTkFrame(master=self.window)
        self.content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=0) #DKInput
        self.content.grid_rowconfigure(2, weight=0) #Buttons


        self.dk_variable = ctk.StringVar()
        self.dke = ctk.CTkEntry(master=self.content, placeholder_text="Enter Decryption Key", textvariable=self.dk_variable, font=("Helvetica", 16))
        self.dke.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        button_frame = ctk.CTkFrame(master=self.content, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.check_button = ctk.CTkButton(master=button_frame, text="Check", command=self.get_dkey, width=120)
        self.check_button.grid(row=0, column=0, padx=10, pady=10)

        self.check_button.configure(state="normal")

    def get_dkey(self):
        self.check_button.configure(state="normal")
        dk = self.dk_variable.get()
        print(f"Your Decryption Key is... {dk}")


app = ctk.CTk()
auth_ui = States(app)
app.mainloop()