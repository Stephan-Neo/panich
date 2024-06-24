import numpy as np

# Функция f(x, t) = (x + 1) * sin(pi * t)
def f(x, t):
    return (x + 1) * np.sin(np.pi * t)

# Начальные условия
def u_initial(t):
    return 1 / (1.01 + t**2)

# Метод Адамса-Моултона для ОДУ
def adams_moulton(f, a, b, u0, t, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    u = np.zeros(n + 1)
    u[0] = u0
    
    for i in range(n):
        u_predict = u[i] + h * f(x[i], t)  # Предсказанное значение методом Эйлера
        u[i + 1] = u[i] + (h / 2) * (f(x[i], t) + f(x[i + 1], t))
        
    return x, u

# Определение порядка сходимости по процессу Эйткена
def aitken(N1, N2, N3):
    if abs(N2 - N3) == 0:
        return np.nan  # or a large number indicating no convergence
    return np.log2(abs(N1 - N2) / abs(N2 - N3))

# Основная функция для выполнения расчетов
def main():
    a, b = -1, 1
    t_values = [0.1, 0.2, 0.5, 0.8, 0.9]
    n_values = [10, 20, 40, 80, 160]
    
    results = {}
    
    for t in t_values:
        results[t] = []
        for n in n_values:
            u0 = u_initial(t)
            x, u = adams_moulton(f, a, b, u0, t, n)
            results[t].append(u[-1])
        
        if len(results[t]) >= 3:
            k = aitken(results[t][-3], results[t][-2], results[t][-1])
            results[t].append(k)
    
    # Вывод результатов
    for t in t_values:
        print(f"t = {t}:")
        for n, u_n in zip(n_values, results[t][:5]):
            print(f"  n = {n}: u(1, t) = {u_n:.10f}")
        if len(results[t]) > 5:
            print(f"  Порядок сходимости: k = {results[t][5]:.4f}")

main()
