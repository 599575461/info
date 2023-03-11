import os


def initializeTS():
    main_list_ts = str()

    for root, dirs, files in os.walk(cwd):
        for name in files:
            if os.path.splitext(name)[1] == ".py":
                main_list_ts += (os.path.join(root, name)) + " "

    os.system(f"C:\\Python39\\Scripts\\pylupdate5.exe {main_list_ts} -ts {cwd}\\QM\\Mainwindow_.ts")


def initializeUI():
    for root, dirs, files in os.walk(f'{cwd}\\UI\\'):
        for name in files:
            new_name = os.path.splitext(name)
            if new_name[1] == ".ui":
                os.system(f"C:\\Python39\\Scripts\\pyuic5.exe {os.path.join(root, name)} -o {cwd}\\Script\\{new_name[0]}.py")


def play_main():
    os.system("python info/Box/Script/main.py")


if __name__ == '__main__':
    cwd = os.getcwd()
    initializeUI()
    initializeTS()
