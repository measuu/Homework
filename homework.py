import numpy as np

#Завдання 1

arr = np.arange(10, 20)

sum_num = np.sum(arr)
print(sum_num)

mean_num = np.mean(arr)
print(mean_num)

min_num = np.min(arr)
print(min_num)

max_num = np.max(arr)
print(max_num)

#Завдання 2

arr = np.random.rand(1000)

sum_num = np.sum(arr)
print(sum_num)

mean_num = np.mean(arr)
print(mean_num)

min_num = np.min(arr)
print(min_num)

max_num = np.max(arr)
print(max_num)

# #Завдання 3

arr = np.random.randint(1, 100, (5, 5))

second_column = arr[:, 1]
second_row = arr[1, :]
flattened = arr.flatten()

print(arr)
print(second_column)
print(second_row)
print(flattened)

# #Завдання 4

arr = np.random.rand(500000)

sum_val = np.sum(arr)
mean_val = np.mean(arr)
min_val = np.min(arr)
max_val = np.max(arr)

print(sum_val)
print(mean_val)
print(min_val)
print(max_val)