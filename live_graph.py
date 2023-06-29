import numpy as np
from time import sleep

filename = "./test_data1.txt"

header = "T_A[K] T_B[K] CNT sr860x[V] sr860y[V] sr860f[Hz] sr860sin[V]\n"

with open(filename, "w") as f:
    f.write(header)
    f.close()

    k = 0

    while True:
        i = np.random.rand()
        line = "%.4f %.4f %d %.6f %.6f %.3f %.1f\n" % (300 + i, 300 - i, k, i, i ** 2, np.sqrt(i), np.sin(i))
        k += 1
        with open(filename, "a") as f:
            f.write(line)
            f.close()
        print(line)
        sleep(2)