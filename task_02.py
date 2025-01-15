import time
import json
from redis import Redis
from hyperloglog import HyperLogLog

def load_data(file_path):
    unique_ips = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line.strip())
                    ip = data.get("remote_addr")
                    if ip:
                        unique_ips.append(ip)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print("Файл не знайдено!")
    return unique_ips

# Точний підрахунок унікальних IP
def count_unique_exact(data):
    return len(set(data))

# Підрахунок унікальних IP за допомогою HyperLogLog
def count_unique_hyperloglog(data):
    hll = HyperLogLog(0.01)  
    for ip in data:
        hll.add(ip)
    return len(hll)

if __name__ == "__main__":
    file_path = "lms-stage-access.log"
    ip_data = load_data(file_path)

    if not ip_data:
        print("Немає даних для аналізу!")
    else:
        # Точний підрахунок
        start_time = time.time()
        exact_count = count_unique_exact(ip_data)
        exact_time = time.time() - start_time

        # HyperLogLog підрахунок
        start_time = time.time()
        hll_count = count_unique_hyperloglog(ip_data)
        hll_time = time.time() - start_time

        # Вивід результатів
        print("Результати порівняння:")
        print(f"{'Метод':<20} {'Унікальні елементи':<20} {'Час виконання (сек.)':<20}")
        print(f"{'-' * 60}")
        print(f"{'Точний підрахунок':<20} {exact_count:<20} {exact_time:<20.5f}")
        print(f"{'HyperLogLog':<20} {hll_count:<20} {hll_time:<20.5f}")
