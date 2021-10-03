from matplotlib import pyplot as plt
import random
from threading import Thread

current_value = 5000
list_of_values = [current_value]

max_val = 100000
min_val = 3000


def stock_sim():
    global current_value, list_of_values, min_val, max_val
    for x in range(100000000):
        if random.randint(1,2) == 2:
            current_value += random.randint(random.randint(10, 20), random.randint(25, 30))
        else:
            current_value -= random.randint(random.randint(10, 20), random.randint(25, 30))

        if current_value > max_val:
            e = random.randint(1,3)
            if e == 1:
                current_value -= random.randint(random.randint(10000, 15000), random.randint(15000, 20000))
            elif e == 2:
                current_value -= random.randint(random.randint(20000, 25000), random.randint(25000, 30000))
            else:
                current_value -= random.randint(random.randint(40000, 45000), random.randint(45000, 50000))
        elif current_value < min_val:
            e = random.randint(1,3)
            if e == 1:
                current_value += random.randint(random.randint(1000, 1500), random.randint(1500, 2000))
            elif e == 2:
                current_value += random.randint(random.randint(2000, 2500), random.randint(2500, 3000))
            else:
                current_value += random.randint(random.randint(4000, 4500), random.randint(4500, 5000))

        list_of_values.append(current_value)


stock_sim()

plt.plot(range(len(list_of_values)), list_of_values)
plt.xlabel('Minutes')
plt.ylabel('Value (GBP)')
plt.title('Botcoin Value (Last Week)')
plt.show()
#plt.savefig('books_read.png')
