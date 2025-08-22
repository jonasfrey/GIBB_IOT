import time 
n_ms = time.ticks_us()
print ('test')
time.sleep_ms(50)
n_ms2 = time.ticks_us()
print(n_ms)
print(n_ms2)
print("Time elapsed:", time.ticks_diff(n_ms2, n_ms), "ms")