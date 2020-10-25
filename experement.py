from threading import Thread
from time import sleep
def func(f):
    print(f)
    for i in range(5):
        print(f"from child thread: {i}")
        sleep(0.5)


th = Thread(target=lambda f='fuck\n': func(f))
th.start()
for i in range(5):
    print(f"from main thread: {i}")
    sleep(1)