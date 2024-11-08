## TODO: Import necessary modules and profiler function
from complexity import time_and_space_profiler
from tqdm import tqdm, trange
import numpy as np
import pandas as pd

## TODO: Set up data generation parameters

np.random.seed(42)
sizes = [100,1000,10000,100000]  # أحجام مختلفة للمصفوفات
tests_per_size = 30  # عدد مرات تنفيذ كل اختبار

# أنواع الترتيب: عشوائي، تصاعدي، تنازلي
def generate_data(size, order="random"):
    if order == "random":
        return np.random.randint(1, 4 * size, size=size)
    elif order == "ascending":
        return np.arange(1, size + 1)
    elif order == "descending":
        return np.arange(size, 0, -1)

# تخزين بيانات الاختبار في قائمة
tests = []
for size in sizes:
    for order in ["random", "ascending", "descending"]:
        for _ in range(tests_per_size):
            arr = generate_data(size, order)
            tests.append((size, order, arr.copy()))

## TODO: Implement Sorting Algorithms with Profiling Decorator
@time_and_space_profiler
def tri_selection(t):
    comparisons, moves = 0, 0
    n = len(t)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if t[j] < t[min_index]:
                min_index = j
        if min_index != i:
            t[i], t[min_index] = t[min_index], t[i]
            moves += 1
    return comparisons, moves

@time_and_space_profiler
def tri_bull(t):
    comparisons, moves = 0, 0
    n = len(t)
    for i in range(n - 1, 0, -1):
        for k in range(i):
            comparisons += 1
            if t[k] > t[k + 1]:
                t[k], t[k + 1] = t[k + 1], t[k]
                moves += 1
    return comparisons, moves

@time_and_space_profiler
def tri_insertion_shifting(t):
    comparisons, moves = 0, 0
    n = len(t)
    for i in range(1, n):
        x = t[i]
        k = i - 1
        while k >= 0 and t[k] > x:
            comparisons += 1
            t[k + 1] = t[k]
            k -= 1
        t[k + 1] = x
        moves += 1
    return comparisons, moves

@time_and_space_profiler
def insertion_sort_exchanges(t):
    comparisons, moves = 0, 0
    n = len(t)
    for i in range(1, n):
        k = i
        while k > 0 and t[k - 1] > t[k]:
            comparisons += 1
            t[k], t[k - 1] = t[k - 1], t[k]
            k -= 1
    return comparisons, moves

## TODO: Benchmark and record results

# List of sorting functions to test
## TODO: Benchmark and record results

# List of sorting functions to test
algorithms = {
    "Selection Sort": tri_selection,
    "Bubble Sort": tri_bull,
    "Insertion Sort (Exchanges)": insertion_sort_exchanges,
    "Insertion Sort (Shifting)": tri_insertion_shifting,
}
results = []

for size, order, arr in tqdm(tests, desc="Sorting Tests", unit="test"):
    for func_name, sort_func in algorithms.items():
        comparisons, moves, cpu_time, memory_usage = sort_func(arr.copy())  # استخدام نسخة من المصفوفة
        results.append((func_name, size, order, comparisons, moves, cpu_time, memory_usage))

# إنشاء DataFrame لتخزين النتائج
df = pd.DataFrame(results, columns=['Function', 'Array Size', 'Order', 'Comparisons', 'Moves', 'CPU Time (s)', 'Memory Usage (MiB)'])

# طباعة النتائج
print(df)

# حفظ النتائج في ملف CSV
df.to_csv('sorting_results.csv', index=False)
