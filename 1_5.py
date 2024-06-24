from math import log, sin, tan
import numpy as np

# Функция для вычисления значений функции на сетке
def function_values(func, x_values):
    return [func(x) for x in x_values]

# Кусочно-постоянная интерполяция
def piecewise_constant(x_values, y_values, x_point):
    for i in range(len(x_values) - 1):
        if x_values[i] <= x_point < x_values[i + 1]:
            return y_values[i]
    return y_values[-1]

# Кусочно-параболическая интерполяция
def piecewise_parabolic(x_values, y_values, x_point):
    for i in range(1, len(x_values) - 1):
        if x_values[i - 1] <= x_point < x_values[i + 1]:
            x0, x1, x2 = x_values[i - 1], x_values[i], x_values[i + 1]
            y0, y1, y2 = y_values[i - 1], y_values[i], y_values[i + 1]
            # Решение системы уравнений для нахождения коэффициентов параболы
            denominator = (x0 - x1) * (x0 - x2) * (x1 - x2)
            a = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / denominator
            b = (x2**2 * (y0 - y1) + x1**2 * (y2 - y0) + x0**2 * (y1 - y2)) / denominator
            c = (x0 * x1 * (y2 - y0) + x1 * x2 * (y0 - y1) + x2 * x0 * (y1 - y2)) / (denominator)
            return a * x_point**2 + b * x_point + c
    # Если x_point не входит в интервал между узлами, используем ближайший узел для интерполяции
    if x_point < x_values[1]:
        return y_values[0]
    return y_values[-1]

# Функция для интерполяции и вычисления нормы отклонения
def interpolate_and_calculate_norm(func, interval, num_nodes, method):
    # Генерируем узлы сетки
    x_values = np.linspace(interval[0], interval[1], num_nodes)
    # Вычисляем значения функции в узлах
    y_values = function_values(func, x_values)
    
    # Точки для вычисления интерполированных значений
    target_x_values = np.linspace(interval[0], interval[1], num_nodes*10)
    # Интерполируем значения
    if method == 'constant':
        interpolated_values = [piecewise_constant(x_values, y_values, x) for x in target_x_values]
    elif method == 'parabolic':
        interpolated_values = [piecewise_parabolic(x_values, y_values, x) for x in target_x_values]
    else:
        raise ValueError("Unknown method specified.")
    
    # Вычисляем точные значения функции для оценки погрешности
    exact_values = function_values(func, target_x_values)
    
    # Вычисляем норму отклонения
    deviation = np.linalg.norm(np.array(exact_values) - np.array(interpolated_values), ord=2) / np.sqrt(len(exact_values))
    return deviation


functions = {
    'ln': {
        'func': log,
        'intervals': [(0.0001, 1)]
    },
    'sin(x) / x': {
        'func': lambda x: sin(x) / x if x != 0 else 1,  # sin(x)/x не определен в x=0, поэтому возвращаем предел 1
        'intervals': [(0.0001, 1), (1, 2)]
    },
    'sin(1 / x)' : {
        'func': lambda x: sin(1/x),
        'intervals': [(0.0001, 1), (1, 2)]
    },
    'tan': {
        'func': tan,
        'intervals': [(0.0, 1.57), (-1, 1)]  # Убираем точку разрыва pi/2 для tan
    }
}


results = {}
node_counts = [2, 4, 8, 16, 32, 64, 128]  # Количество узлов для интерполяции


for name, data in functions.items():
    func = data['func']
    results[name] = {}
    for interval in data['intervals']:
        interval_results = {}
        for count in node_counts:
            const_norm = interpolate_and_calculate_norm(func, interval, count, 'constant')
            parab_norm = interpolate_and_calculate_norm(func, interval, count, 'parabolic')
            interval_results[count] = {'constant': const_norm, 'parabolic': parab_norm}
        results[name][interval] = interval_results


for name, intervals in results.items():
    print(f"Function: {name}")
    for interval, counts in intervals.items():
        print(f" Interval: {interval}")
        for count, methods in counts.items():
            print(f"  Nodes: {count}")
            for method, norm in methods.items():
                print(f"   Method: {method}, Norm: {norm}")
    print() 
