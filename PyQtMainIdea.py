import os


def initializeTS():
    main_list_ts = str()

    for root, dirs, files in os.walk('Script'):
        for name in files:
            if os.path.splitext(name)[1] == ".py":
                main_list_ts += (os.path.join(root, name)) + " "

    os.system(fr"C:\Python39\Scripts\pylupdate5.exe {main_list_ts} -ts ./QM/Mainwindow_.ts")


def initializeUI():
    for root, dirs, files in os.walk('UI'):
        for name in files:
            new_name = os.path.splitext(name)
            if new_name[1] == ".ui":
                os.system(fr"C:\Python39\Scripts\pyuic5.exe {os.path.join(root, name)} -o Script/{new_name[0]}.py")


def play_main():
    os.system("python Script/main.py")


if __name__ == '__main__':
    initializeUI()
    initializeTS()
    play_main()
