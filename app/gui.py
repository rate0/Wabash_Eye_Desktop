import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Label, Frame, Button
from face_manager import authenticate_user_from_image, add_user_from_image, user_exists_by_name, user_exists_by_face
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wabash Eye")
        self.configure(bg='#330000')  # Темно-красный фон

        # Развертывание окна на весь экран
        self.attributes('-fullscreen', True)

        self.create_widgets()

    def create_widgets(self):
        # Создание фрейма для заголовка
        header_frame = Frame(self, bg='#330000')
        header_frame.pack(fill='x')

        # Заголовок приложения
        header_label = Label(header_frame, text="Wabash Eye", font=("Arial", 24, "bold"), fg="white", bg="#330000")
        header_label.pack(pady=20)

        # Фрейм для кнопок
        button_frame = Frame(self, bg='#330000')
        button_frame.pack(fill='both', expand=True, pady=50)

        # Настройка кнопок
        self.setup_buttons(button_frame)

    def setup_buttons(self, button_frame):
        button_color = '#660000'  # Темно-красный
        text_color = 'white'  # Белый текст

        self.register_button = Button(button_frame, text="Register New User", command=self.register_user, width=20, height=2, font=("Arial", 14), bg=button_color, fg=text_color)
        self.register_button.pack(pady=20)

        self.authenticate_button = Button(button_frame, text="Authenticate from Image", command=self.authenticate, width=20, height=2, font=("Arial", 14), bg=button_color, fg=text_color)
        self.authenticate_button.pack(pady=20)

        self.process_images_button = Button(button_frame, text="Process Images from Folder", command=self.process_images_from_folder, width=25, height=2, font=("Arial", 14), bg=button_color, fg=text_color)
        self.process_images_button.pack(pady=20)

        self.exit_fullscreen_button = Button(button_frame, text="Exit Fullscreen", command=self.exit_fullscreen, width=20, height=2, font=("Arial", 14), bg=button_color, fg=text_color)
        self.exit_fullscreen_button.pack(pady=20)

    def register_user(self):
        username = simpledialog.askstring("Input", "What is your username?", parent=self)
        if username:
            if user_exists_by_name(username):
                messagebox.showerror("Registration", "User with this name already exists.")
                return

            file_path = filedialog.askopenfilename()
            if file_path:
                if user_exists_by_face(file_path):
                    messagebox.showerror("Registration", "User with this face already exists.")
                    return

                add_user_from_image(username, file_path)
                messagebox.showinfo("Registration", "User has been registered successfully.")
            else:
                messagebox.showinfo("Registration", "No file selected.")
        else:
            messagebox.showinfo("Registration", "Registration cancelled.")

    def authenticate(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            username = authenticate_user_from_image(file_path)
            if username:
                messagebox.showinfo("Authentication", f"Authenticated as {username}")
                user_folder_path = os.path.abspath(os.path.join('resources', 'user_folders', username))
                if not os.path.exists(user_folder_path):
                    os.makedirs(user_folder_path)
                os.system(f"xterm -e 'cd {user_folder_path} && /bin/bash'")
            else:
                messagebox.showerror("Authentication", "Authentication failed.")
        else:
            messagebox.showinfo("Authentication", "No file selected.")

    def process_images_from_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            user_images_dir = os.path.join(folder_path, 'user_images')
            if not os.path.exists(user_images_dir):
                messagebox.showerror("Error", "The specified folder does not exist or does not contain a 'user_images' subfolder.")
                return

            for image_name in os.listdir(user_images_dir):
                image_path = os.path.join(user_images_dir, image_name)
                try:
                    parts = image_name.split('_')
                    if len(parts) >= 5:
                        firstname = parts[0]
                        lastname = parts[1]
                        username = f"{firstname}_{lastname}"
                        if not user_exists_by_name(username):
                            add_user_from_image(username, image_path)
                        else:
                            print(f"User {username} already exists. Skipping.")
                    else:
                        print(f"Filename {image_name} does not match the expected format. Skipping.")
                except Exception as e:
                    print(f"An error occurred while processing {image_name}: {e}")
            messagebox.showinfo("Process Completed", "All images have been processed.")
        else:
            messagebox.showinfo("Process Images", "No folder selected.")

    def exit_fullscreen(self):
        self.attributes('-fullscreen', False)
        self.exit_fullscreen_button.pack_forget()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
