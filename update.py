#            ╔═════════════════════════HaZaRd═════════════════════════════╗
#            ║        Youtube: https://www.youtube.com/@IIIHaZaRd         ║
#            ║        Github: https://github.com/Pytholearn               ║
#            ║        Discord: https://discord.gg/YU7jYRkxwp              ║
#            ╚════════════════════════════════════════════════════════════╝
import customtkinter
import os
import git
import shutil
import AutoUpdate.CFU
from plyer import notification



def check_for_update():
    cwd = os.getcwd()
    AutoUpdate.CFU.set_url("https://raw.githubusercontent.com/Pytholearn/HAZARD-CHAMELEONS/main/version")
    download_link = "https://github.com/Pytholearn/HAZARD-CHAMELEONS.git"
    AutoUpdate.CFU.set_current_version("1.1.3")

    if not AutoUpdate.CFU.is_up_to_date():
        root = customtkinter.CTk()
        root.geometry("600x400")
        root.title("Check for Update")

        status_label = customtkinter.CTkLabel(root, text="New Update Available!\nWould you like to update your tool?", font=("Arial", 16))
        status_label.pack(pady=20)
        notification.notify(
        title='New Update',
        message='New Update Found!',
        app_name='Guard Password Manager',
        timeout=3, 
        app_icon='5582931.ico'  
        )

        def on_yes():
            local_repo_path = os.path.join(cwd, "temp_repo")
            if not os.path.exists(local_repo_path):
                os.makedirs(local_repo_path)
            git.Repo.clone_from(download_link, local_repo_path)
            #Made 
            for root_dir, dirs, files in os.walk(local_repo_path):
                relative_path = os.path.relpath(root_dir, local_repo_path)
                for file in files:#by
                    source_file_path = os.path.join(root_dir, file)
                    dest_file_path = os.path.join(cwd, relative_path, file)
                    if os.path.exists(dest_file_path):
                        os.remove(dest_file_path)  
                    shutil.move(source_file_path, dest_file_path)  
                for dir in dirs:#HAZARD
                    source_dir_path = os.path.join(root_dir, dir)
                    dest_dir_path = os.path.join(cwd, relative_path, dir)
                    if not os.path.exists(dest_dir_path):
                        shutil.move(source_dir_path, dest_dir_path) 

            shutil.rmtree(local_repo_path)
            root.destroy()
            os._exit(0) 

        def on_no():
            root.destroy()
            return False

        yes_button = customtkinter.CTkButton(root, text="Yes", command=on_yes)
        yes_button.pack(pady=10)

        no_button = customtkinter.CTkButton(root, text="No", command=on_no)
        no_button.pack(pady=10)

        root.mainloop()
        return True
    else:
        return
    
#            ╔═════════════════════════HaZaRd═════════════════════════════╗
#            ║        Youtube: https://www.youtube.com/@IIIHaZaRd         ║
#            ║        Github: https://github.com/Pytholearn               ║
#            ║        Discord: https://discord.gg/YU7jYRkxwp              ║
#            ╚════════════════════════════════════════════════════════════╝