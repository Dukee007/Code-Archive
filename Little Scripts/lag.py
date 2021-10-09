import threading, random, time

ramm = {}

next_k = 100

def maths():
    global ramm

    while 1:
        ramm[int(random.randint(11111111111, 999999999999999))] = ramm
        ramm[int(random.randint(11111111111, 999999999999999))] = int(random.randint(11111111111, 999999999999999))*int(random.randint(11111111111, 999999999999999))

for i in range(1):
    if i == next_k:
        print(f"loading thread {i}")
        next_k = i+100

    threading.Thread(target=maths).start()
