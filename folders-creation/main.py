import os

def create_folders(path, num):
    
    os.makedirs(path, exist_ok=True)
    for i in range(1, num + 1):
        
        folder_name = f"proyecto {i}"
        
        folder_path = os.path.join(path, folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created: {folder_path}")
        
create_folders(
    "C:/organiza/con/python",
    1000)