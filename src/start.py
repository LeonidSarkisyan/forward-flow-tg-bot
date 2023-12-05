import threading
import os


def thread_one():
    os.system("python -m src.main")


def thread_two():
    os.system("python -m src.userbot")


if __name__ == "__main__":
    t1 = threading.Thread(target=thread_one)
    t2 = threading.Thread(target=thread_two)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
