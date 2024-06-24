import numpy as np

# Функция, которую будем интегрировать
def f(x):
    return np.exp(x) + x**2

# Метод левых прямоугольников
def left_rectangles(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b - h, n)  # узлы слева
    return h * np.sum(f(x))

# Метод центральных прямоугольников
def mid_rectangles(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a + h / 2, b - h / 2, n)  # середины отрезков
    return h * np.sum(f(x))

# Процесс Эйткена для определения порядка сходимости
def aitken(N1, N2, N3):
    return np.log2(abs(N1 - N2) / abs(N2 - N3))

# Интервал интегрирования
a, b = 0, 2

# Значения n
n_values = [10, 20, 40]

# Вычисление интегралов методом левых прямоугольников
left_results = [left_rectangles(f, a, b, n) for n in n_values]

# Вычисление интегралов методом центральных прямоугольников
mid_results = [mid_rectangles(f, a, b, n) for n in n_values]

# Определение порядка сходимости по процессу Эйткена
k_left = aitken(left_results[0], left_results[1], left_results[2])
k_mid = aitken(mid_results[0], mid_results[1], mid_results[2])

# Вывод результатов
print("Метод левых прямоугольников:")
for n, result in zip(n_values, left_results):
    print(f"n = {n}: интеграл = {result:.10f}")
print(f"Порядок сходимости (левые прямоугольники): k = {k_left:.4f}")

print("\nМетод центральных прямоугольников:")
for n, result in zip(n_values, mid_results):
    print(f"n = {n}: интеграл = {result:.10f}")
print(f"Порядок сходимости (центральные прямоугольники): k = {k_mid:.4f}")