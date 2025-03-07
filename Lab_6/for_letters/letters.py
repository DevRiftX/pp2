# 6

import os
import string

directory_folder = r"C:\Users\admin\Desktop\KBTU\Python\PP2\pp2\Lab_6\for_letters"

if not os.path.exists(directory_folder):
    os.makedirs(directory_folder)

for letter in string.ascii_uppercase:
    file_path = os.path.join(directory_folder, f"{letter}.txt")
    with open(file_path, 'w') as file:
        file.write(f"{letter}.txt was created successfully\n")

print("All files created successfully!")
