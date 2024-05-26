import numpy as np

def rk4(f, y0, t0, tf, n):
    h = (tf - t0) / n
    t = np.linspace(t0, tf, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    
    for i in range(n):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(t[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(t[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    
    return t, y

def aitken(y_n, y_n1, y_n2):
    return y_n - ((y_n1 - y_n)**2) / (y_n2 - 2*y_n1 + y_n)

def convergence_order(y_values, n_values):
    orders = []
    for i in range(1, len(n_values) - 1):
        y1, y2, y3 = y_values[i-1], y_values[i], y_values[i+1]
        h1, h2 = 2/n_values[i-1], 2/n_values[i]
        order = (np.log(abs(y2 - y1)) - np.log(abs(y3 - y2))) / (np.log(h2) - np.log(h1))
        orders.append(order)
    return orders

# Пример функции ОДУ
def f(t, y):
    return -2 * t * y  # пример, можно заменить на другую

# Начальные условия и параметры
t0, tf, y0 = 0, 1, 1  # начальные условия, можно изменить
n_values = [10, 20, 40, 80, 160]

# Решения для разных n
solutions = []
for n in n_values:
    t, y = rk4(f, y0, t0, tf, n)
    solutions.append(y[-1])

# Процесс Эйткена для численного решения
solutions_aitken = []
for i in range(len(solutions) - 2):
    y_aitken = aitken(solutions[i], solutions[i + 1], solutions[i + 2])
    solutions_aitken.append(y_aitken)

# Вычисление порядка сходимости
orders = convergence_order(solutions, n_values)

print("Решения для различных n:", solutions)
print("Уточненные решения (процесс Эйткена):", solutions_aitken)
print("Порядок сходимости:", orders)
