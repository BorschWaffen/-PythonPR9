import json
import os

# Назва файлу для збереження даних
DATA_FILE = "football_teams.json"
RESULTS_FILE = "championship_results.json"

# Початкові дані (10 команд з різною кількістю очок)
initial_data = [
    {"name": "Динамо", "points": 75},
    {"name": "Шахтар", "points": 82},
    {"name": "Дніпро", "points": 58},
    {"name": "Зоря", "points": 65},
    {"name": "Ворскла", "points": 52},
    {"name": "Олександрія", "points": 48},
    {"name": "Львів", "points": 44},
    {"name": "Колос", "points": 41},
    {"name": "Маріуполь", "points": 38},
    {"name": "Минай", "points": 35}
]

def initialize_data():
    """Ініціалізація JSON файлу з початковими данами"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
    print("Файл з даними ініціалізовано!")

def display_data():
    """Виведення вмісту JSON файлу на екран"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n--- ДАНІ ПРО КОМАНДИ ---")
        for i, team in enumerate(data, 1):
            print(f"{i}. {team['name']}: {team['points']} очок")
        print()
    except FileNotFoundError:
        print("Файл з даними не знайдено! Спочатку ініціалізуйте дані.")

def add_team():
    """Додавання нової команди"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n--- ДОДАВАННЯ НОВОЇ КОМАНДИ ---")
        name = input("Введіть назву команди: ")
        
        # Перевірка на унікальність назви
        for team in data:
            if team['name'].lower() == name.lower():
                print("Команда з такою назвою вже існує!")
                return
        
        # Перевірка на унікальність очок
        while True:
            try:
                points = int(input("Введіть кількість очок: "))
                
                # Перевірка на унікальність очок
                points_exist = False
                for team in data:
                    if team['points'] == points:
                        points_exist = True
                        break
                
                if points_exist:
                    print("Команда з такою кількістю очок вже існує! Очки мають бути унікальними.")
                else:
                    break
            except ValueError:
                print("Будь ласка, введіть ціле число!")
        
        # Додавання нової команди
        new_team = {"name": name, "points": points}
        data.append(new_team)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Команда '{name}' успішно додана!")
        
    except FileNotFoundError:
        print("Файл з даними не знайдено! Спочатку ініціалізуйте дані.")

def remove_team():
    """Видалення команди"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n--- ВИДАЛЕННЯ КОМАНДИ ---")
        display_data()
        
        name = input("Введіть назву команди для видалення: ")
        
        # Пошук команди за назвою
        found = False
        for i, team in enumerate(data):
            if team['name'].lower() == name.lower():
                del data[i]
                found = True
                break
        
        if found:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Команда '{name}' успішно видалена!")
        else:
            print(f"Команда '{name}' не знайдена!")
            
    except FileNotFoundError:
        print("Файл з даними не знайдено! Спочатку ініціалізуйте дані.")

def search_teams():
    """Пошук команд за назвою або кількістю очок"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n--- ПОШУК КОМАНД ---")
        print("1. Пошук за назвою")
        print("2. Пошук за кількістю очок")
        
        choice = input("Виберіть тип пошуку (1 або 2): ")
        
        if choice == '1':
            name = input("Введіть назву команди для пошуку: ")
            found_teams = [team for team in data if name.lower() in team['name'].lower()]
        elif choice == '2':
            try:
                points = int(input("Введіть кількість очок для пошуку: "))
                found_teams = [team for team in data if team['points'] == points]
            except ValueError:
                print("Будь ласка, введіть ціле число!")
                return
        else:
            print("Невірний вибір!")
            return
        
        if found_teams:
            print("\n--- РЕЗУЛЬТАТИ ПОШУКУ ---")
            for team in found_teams:
                print(f"{team['name']}: {team['points']} очок")
        else:
            print("Команди не знайдено!")
            
    except FileNotFoundError:
        print("Файл з даними не знайдено! Спочатку ініціалізуйте дані.")

def calculate_championship_results():
    """Визначення чемпіона та призерів"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Сортування команд за кількістю очок (за спаданням)
        sorted_teams = sorted(data, key=lambda x: x['points'], reverse=True)
        
        # Визначення результатів
        champion = sorted_teams[0] if len(sorted_teams) > 0 else None
        second_place = sorted_teams[1] if len(sorted_teams) > 1 else None
        third_place = sorted_teams[2] if len(sorted_teams) > 2 else None
        
        # Формування результату
        results = {
            "champion": champion,
            "second_place": second_place,
            "third_place": third_place,
            "all_teams_sorted": sorted_teams
        }
        
        # Виведення результатів на екран
        print("\n--- РЕЗУЛЬТАТИ ЧЕМПІОНАТУ ---")
        if champion:
            print(f"🏆 ЧЕМПІОН: {champion['name']} - {champion['points']} очок")
        if second_place:
            print(f"🥈 ДРУГЕ МІСЦЕ: {second_place['name']} - {second_place['points']} очок")
        if third_place:
            print(f"🥉 ТРЕТЄ МІСЦЕ: {third_place['name']} - {third_place['points']} очок")
        
        # Запис результатів у файл
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\nРезультати збережено у файл: {RESULTS_FILE}")
        
    except FileNotFoundError:
        print("Файл з даними не знайдено! Спочатку ініціалізуйте дані.")

def main_menu():
    """Головне меню програми"""
    while True:
        print("\n" + "="*50)
        print("ПРОГРАМА ДЛЯ РОБОТИ З ДАНИМИ ФУТБОЛЬНОГО ЧЕМПІОНАТУ")
        print("="*50)
        print("1. Вивести дані про команди")
        print("2. Додати нову команду")
        print("3. Видалити команду")
        print("4. Пошук команд")
        print("5. Визначити чемпіона та призерів")
        print("6. Ініціалізувати початкові дані")
        print("0. Вихід")
        print("-"*50)
        
        choice = input("Виберіть опцію (0-6): ")
        
        if choice == '1':
            display_data()
        elif choice == '2':
            add_team()
        elif choice == '3':
            remove_team()
        elif choice == '4':
            search_teams()
        elif choice == '5':
            calculate_championship_results()
        elif choice == '6':
            initialize_data()
        elif choice == '0':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Невірний вибір! Будь ласка, спробуйте ще раз.")

# Запуск програми
if __name__ == "__main__":
    # Перевірка чи існує файл з даними
    if not os.path.exists(DATA_FILE):
        print("Файл з даними не знайдено. Ініціалізую початкові дані...")
        initialize_data()
    
    main_menu()