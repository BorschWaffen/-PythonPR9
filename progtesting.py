# test_program.py - файл для тестування основних функцій

import json

def test_championship_calculation():
    """Тестування функції визначення чемпіона та призерів"""
    
    # Тестові дані
    test_data = [
        {"name": "Динамо", "points": 75},
        {"name": "Шахтар", "points": 82},
        {"name": "Зоря", "points": 65}
    ]
    
    # Збереження тестових даних
    with open("test_data.json", 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    # Завантаження та обробка даних
    with open("test_data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Сортування та визначення результатів
    sorted_teams = sorted(data, key=lambda x: x['points'], reverse=True)
    
    print("ТЕСТУВАННЯ РОЗРАХУНКУ РЕЗУЛЬТАТІВ:")
    print(f"Чемпіон: {sorted_teams[0]['name']} ({sorted_teams[0]['points']} очок)")
    print(f"Друге місце: {sorted_teams[1]['name']} ({sorted_teams[1]['points']} очок)")
    print(f"Третє місце: {sorted_teams[2]['name']} ({sorted_teams[2]['points']} очок)")

if __name__ == "__main__":
    test_championship_calculation()