#            ╔═════════════════════════HaZaRd═════════════════════════════╗
#            ║        Youtube: https://www.youtube.com/@IIIHaZaRd         ║
#            ║        Github: https://github.com/Pytholearn               ║
#            ║        Discord: https://discord.gg/YU7jYRkxwp              ║
#            ╚════════════════════════════════════════════════════════════╝

import customtkinter
import webbrowser
import pyperclip  
import base64
import os
import json
from update import check_for_update
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from plyer import notification

check_for_update()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("1080x720")
root.iconbitmap('5582931.ico')  
root.title("Guard Password Manager - HAZARD & Nothing")

notification.notify(
title='Open App',
message='Guard_Password_Manager Open Now!',
app_name='Guard Password Manager',
timeout=3, 
app_icon='5582931.ico'  
)


def generate_key():
    return os.urandom(32)
def encrypt_aes256(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted_data
def decrypt_aes256(encrypted_data, key):
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()
def save_password_to_file(name, password):
    key = generate_key()
    encrypted_password = encrypt_aes256(password.encode('utf-8'), key)
    with open('passwords.json', 'a') as file:
        data = {
            'name': name,
            'key': base64.b64encode(key).decode(),
            'encrypted_password': base64.b64encode(encrypted_password).decode()
        }
        json.dump(data, file)
        file.write('\n')
def load_passwords_from_file():
    passwords = []
    try:
        with open('passwords.json', 'r') as file:
            for line in file:
                data = json.loads(line)
                key = base64.b64decode(data['key'])
                encrypted_password = base64.b64decode(data['encrypted_password'])
                decrypted_password = decrypt_aes256(encrypted_password, key).decode('utf-8')
                passwords.append({
                    'name': data['name'],
                    'password': decrypted_password
                })
    except FileNotFoundError:
        pass
    return passwords
def delete_password_from_file(name):
    passwords = load_passwords_from_file()
    with open('passwords.json', 'w') as file:
        for pwd in passwords:
            if pwd['name'] != name:
                key = generate_key()  
                encrypted_password = encrypt_aes256(pwd['password'].encode('utf-8'), key)
                data = {
                    'name': pwd['name'],
                    'key': base64.b64encode(key).decode(),
                    'encrypted_password': base64.b64encode(encrypted_password).decode()
                }
                json.dump(data, file)
                file.write('\n')
def open_new_password_form():
    for widget in root.winfo_children():
        widget.pack_forget()
    form_frame = customtkinter.CTkFrame(master=root)
    form_frame.pack(pady=20, padx=60, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=form_frame, text="Enter password details:", font=("Arial", 16))
    label.pack(pady=20, padx=20)
    name_label = customtkinter.CTkLabel(master=form_frame, text="Name:")
    name_label.pack(pady=(0, 5))
    name_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Password Name")
    name_entry.pack(pady=12, padx=10)
    password_label = customtkinter.CTkLabel(master=form_frame, text="Password:")
    password_label.pack(pady=(10, 5))
    password_entry = customtkinter.CTkEntry(master=form_frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)
    ok_button = customtkinter.CTkButton(master=form_frame, text="OK", command=lambda: save_password(name_entry.get(), password_entry.get()))
    ok_button.pack(pady=10, padx=10)
    back_button = customtkinter.CTkButton(master=form_frame, text="Back", command=show_main_page)
    back_button.pack(pady=10, padx=10)
def show_main_page():
    for widget in root.winfo_children():
        widget.pack_forget()
    main_frame = customtkinter.CTkScrollableFrame(root)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=main_frame, text="Guard Password Manager", font=("Arial", 24, "bold"))
    label.pack(pady=20, padx=20)
    new_button = customtkinter.CTkButton(master=main_frame, text="NEW+", command=open_new_password_form)
    new_button.pack(pady=10, padx=10)
    info_button = customtkinter.CTkButton(master=main_frame, text="Info", command=open_info_window)
    info_button.pack(pady=10, padx=10)
    passwords = load_passwords_from_file()
    for item in passwords:
        pwd_frame = customtkinter.CTkFrame(master=main_frame)
        pwd_frame.pack(pady=5, padx=10, fill="x")
        name_label = customtkinter.CTkLabel(master=pwd_frame, text=item['name'], font=("Arial", 14, "bold"))
        name_label.pack(side="left", padx=(0, 10))
        show_button = customtkinter.CTkButton(master=pwd_frame, text="Show", width=60, height=20, font=("Arial", 12), command=lambda pwd=item['password']: open_show_password(pwd))
        show_button.pack(side="right", padx=(0, 10))
        delete_button = customtkinter.CTkButton(master=pwd_frame, text="Delete", width=60, height=20, font=("Arial", 12), command=lambda name=item['name']: confirm_delete(name))
        delete_button.pack(side="right", padx=(0, 10))
def confirm_delete(name):
    def delete_action():
        delete_password_from_file(name)
        confirmation_window.destroy()
        show_main_page()
    def cancel_action():
        confirmation_window.destroy()
    confirmation_window = customtkinter.CTkToplevel(root)
    confirmation_window.geometry("400x200")
    confirmation_window.title("Confirm Delete")
    message_label = customtkinter.CTkLabel(master=confirmation_window, text="Are you sure you want to delete this password?", font=("Arial", 14))
    message_label.pack(pady=20, padx=20)
    yes_button = customtkinter.CTkButton(master=confirmation_window, text="Yes", command=delete_action)
    yes_button.pack(pady=10, padx=10)
    no_button = customtkinter.CTkButton(master=confirmation_window, text="No", command=cancel_action)
    no_button.pack(pady=10, padx=10)
def open_show_password(password):
    for widget in root.winfo_children():
        widget.pack_forget()
    show_frame = customtkinter.CTkFrame(master=root)
    show_frame.pack(pady=20, padx=60, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=show_frame, text="Password:", font=("Arial", 16))
    label.pack(pady=20, padx=20)
    password_label = customtkinter.CTkLabel(master=show_frame, text=password, font=("Arial", 14))
    password_label.pack(pady=10, padx=20)
    copy_button = customtkinter.CTkButton(master=show_frame, text="Copy", command=lambda: copy_to_clipboard(password))
    copy_button.pack(pady=10, padx=10)
    back_button = customtkinter.CTkButton(master=show_frame, text="Back", command=show_main_page)
    back_button.pack(pady=10, padx=10)
def save_password(name, password):
    save_password_to_file(name, password)
    show_main_page()
def copy_to_clipboard(password):
    pyperclip.copy(password)
    copied_label = customtkinter.CTkLabel(master=root, text="Password copied!", text_color="green", font=("Arial", 12, "italic"))
    copied_label.pack(pady=10)
    root.after(2000, copied_label.pack_forget)
def open_info_window():
    info_window = customtkinter.CTkToplevel(root)
    info_window.geometry("500x400")
    info_window.title("Info")
    def open_github():
        webbrowser.open("https://github.com/Pytholearn")
        webbrowser.open("https://github.com/Nomthing")
    github_button = customtkinter.CTkButton(master=info_window, text="Github", command=open_github)
    github_button.pack(pady=10, padx=10)
    def copy_discord_link():
        discord_link = "https://discord.gg/qD8SXrRJbw"
        pyperclip.copy(discord_link)
        copied_label = customtkinter.CTkLabel(master=info_window, text="Discord link copied!", text_color="green")
        copied_label.pack(pady=5, padx=5)
    discord_button = customtkinter.CTkButton(master=info_window, text="Discord", command=copy_discord_link)
    discord_button.pack(pady=10, padx=10)
    def update_action():
        check_for_update()
    update_button = customtkinter.CTkButton(master=info_window, text="Update", command=update_action)
    update_button.pack(pady=10, padx=10)
    author_label = customtkinter.CTkLabel(master=info_window, text="""
Code By: HAZARD & Nothing
Email: police123456789ilia@gmail.com
IRAN ON TOP
Written in history: 2024/3/10
ⓒ Copyright                                   
 """)
    author_label.pack(pady=20, padx=10)
    back_button = customtkinter.CTkButton(master=info_window, text="Back", command=info_window.destroy)
    back_button.pack(pady=10, padx=10)
show_main_page()
root.mainloop()
#            ╔═════════════════════════HaZaRd═════════════════════════════╗
#            ║        Youtube: https://www.youtube.com/@IIIHaZaRd         ║
#            ║        Github: https://github.com/Pytholearn               ║
#            ║        Discord: https://discord.gg/YU7jYRkxwp              ║
#            ╚════════════════════════════════════════════════════════════╝