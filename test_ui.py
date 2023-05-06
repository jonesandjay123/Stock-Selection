import os
import datetime

def create_folder_and_file():
    today = datetime.date.today()
    folder_name = f"{today}_csv"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        file_path = os.path.join(folder_name, "test.csv")
        with open(file_path, "w") as file:
            file.write("This is a test file.\n")
    else:
        print(f"The folder '{folder_name}' already exists. No further action is needed.")

if __name__ == "__main__":
    create_folder_and_file()
