import numpy as np

def f(x):
    # Определите подынтегральную функцию
    return np.sin(x)  # Пример функции

def right_rectangle(f, a, b, n):
    h = (b - a) / n
    result = 0
    for i in range(n):
        result += f(a + i * h)
    return result * h

def trapezoidal(f, a, b, n):
    h = (b - a) / n
    result = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        result += f(a + i * h)
    return result * h

def runge_refinement(I1, I2, k):
    return I2 + (I2 - I1) / (2**k - 1)

def aitken_process(I1, I2, I3):
    return I1 - (I2 - I1)**2 / (I3 - 2*I2 + I1)

def calculate_integral(f, a, b, ns, method):
    results = []
    for n in ns:
        if method == 'right_rectangle':
            result = right_rectangle(f, a, b, n)
        elif method == 'trapezoidal':
            result = trapezoidal(f, a, b, n)
        results.append(result)
    return results

# Параметры задачи
a = 0  # Начало интервала
b = np.pi  # Конец интервала
ns = [10, 20, 40, 80]  # Число разбиений

# Вычисление интегралов
integrals_right_rect = calculate_integral(f, a, b, ns, 'right_rectangle')
integrals_trapezoidal = calculate_integral(f, a, b, ns, 'trapezoidal')

# Повышение точности по методу Рунге
integrals_right_rect_runge = [
    runge_refinement(integrals_right_rect[i], integrals_right_rect[i + 1], 1) for i in range(len(ns) - 1)
]
integrals_trapezoidal_runge = [
    runge_refinement(integrals_trapezoidal[i], integrals_trapezoidal[i + 1], 2) for i in range(len(ns) - 1)
]

# Численный порядок сходимости методом Эйткена
right_rect_orders = [
    aitken_process(integrals_right_rect[i], integrals_right_rect[i + 1], integrals_right_rect[i + 2]) for i in range(len(ns) - 2)
]
trapezoidal_orders = [
    aitken_process(integrals_trapezoidal[i], integrals_trapezoidal[i + 1], integrals_trapezoidal[i + 2]) for i in range(len(ns) - 2)
]

# Печать результатов
print("Интегралы методом правых прямоугольников:", integrals_right_rect)
print("Интегралы методом правых прямоугольников с уточнением Рунге:", integrals_right_rect_runge)
print("Порядок сходимости методом правых прямоугольников по Эйткену:", right_rect_orders)

print("Интегралы методом трапеций:", integrals_trapezoidal)
print("Интегралы методом трапеций с уточнением Рунге:", integrals_trapezoidal_runge)
print("Порядок сходимости методом трапеций по Эйткену:", trapezoidal_orders)
