# Импортируйте необходимые модули

from datetime import datetime

FORMAT = "%H:%M:%S"  # Запишите формат полученного времени.
WEIGHT = 75  # Вес.
HEIGHT = 175  # Рост.
K_1 = 0.035  # Коэффициент для подсчета калорий.
K_2 = 0.029  # Коэффициент для подсчета калорий.
STEP_M = 0.65  # Длина шага в метрах.

storage_data = {}  # Словарь для хранения полученных данных.


def time_to_seconds(time_str):
    """Секунды от полуночи для сравнения времён по FORMAT."""
    t = datetime.strptime(time_str, FORMAT).time()
    return t.hour * 3600 + t.minute * 60 + t.second


def check_correct_data(data):
    """Проверка корректности полученного пакета."""
    if len(data) != 2 or data[0] == "" or data[1] == "":
        return False
    return True

def check_correct_time(time):
    """Проверка корректности параметра времени."""
    if len(storage_data) == 0:
        return True
    try:
        new_sec = time_to_seconds(time)
    except (ValueError, TypeError):
        return False
    max_sec = max(time_to_seconds(k) for k in storage_data)
    return new_sec > max_sec


def get_step_day(steps):
    """Получить количество пройденных шагов за этот день."""
    # Посчитайте все шаги, записанные в словарь storage_data,
    # прибавьте к ним значение из последнего пакета
    # и верните  эту сумму.
    return sum(storage_data.values())

def get_distance(steps):
    """Получить дистанцию пройденного пути в км."""
    # Посчитайте дистанцию в километрах,
    # исходя из количества шагов и длины шага.
    return get_step_day(steps) * STEP_M / 1000
    
def get_mean_speed(distance, time_in_minutes):
    """Получить среднюю скорость движения."""
    return distance / time_in_minutes

def get_spent_calories(dist, current_time):
    """Получить значения потраченных калорий."""
    # В уроке «Последовательности» вы написали формулу расчета калорий.
    time_parts = current_time.split(":")
    h, m, s = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
    seconds_since_midnight = h * 3600 + m * 60 + s
    time_in_minutes = max(seconds_since_midnight / 60.0, 1e-9)

    spent_calories = (
        K_1 * WEIGHT
        + (
            (get_mean_speed(dist, time_in_minutes) ** 2 / HEIGHT)
            * K_2
            * WEIGHT
        )
        * time_in_minutes
    )
    return spent_calories


def get_achievements(distance_km):
    if distance_km >= 6.5:
        return "Отличный результат! Цель достигнута."
    elif distance_km >= 3.9:
        return "Неплохо! День был продуктивный"
    elif distance_km >= 2:
        return "Завтра наверстаем!"
    else:
        return "Лежать тоже полезно. Главное — участие, а не победа!"

def show_message(time, step_day, distance, spent_calories, achievements):
    print(f"\nВремя: {time}.")
    print(f"Количество шагов за сегодня: {step_day}.")
    print(f"Дистанция составила {distance:.2f} км.")
    print(f"Вы сожгли {spent_calories:.2f} ккал.")
    print(f"{achievements}")
    print("\n")

def accept_package(package):
    """Принять пакет."""
    if not check_correct_data(package):
        print("Некорректный пакет")
        return storage_data

    try:
        new_sec = time_to_seconds(package[0])
    except (ValueError, TypeError):
        print("Некорректный пакет")
        return storage_data

    if len(storage_data) > 0:
        max_sec = max(time_to_seconds(k) for k in storage_data)
        if new_sec < max_sec:
            storage_data.clear()

    if not check_correct_time(package[0]):
        print("Некорректный пакет")
        return storage_data

    storage_data[package[0]] = package[1]

    total_steps = get_step_day(package[1])
    dist = get_distance(package[1])
    achievements = get_achievements(dist)
    spent = get_spent_calories(dist, package[0])
    show_message(package[0], total_steps, dist, spent, achievements)

    return storage_data

def main():
    while True:
        package = input(), int(input())
        if package[0] == "0:00:00":
            break
        accept_package(package)

if __name__ == "__main__":
    main()
