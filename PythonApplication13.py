import csv
import os

def display_csv_file(filename):
    """Функція для виведення вмісту CSV файлу на екран"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            print(f"\n{'='*80}")
            print(f"ВМІСТ ФАЙЛУ: {filename}")
            print(f"{'='*80}")
            
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Читаємо заголовки
            
            # Виводимо заголовки
            print(" | ".join(headers))
            print("-" * 80)
            
            # Виводимо дані
            row_count = 0
            for row in csv_reader:
                print(" | ".join(row))
                row_count += 1
                
            print(f"{'='*80}")
            print(f"Всього рядків: {row_count}")
            print(f"{'='*80}")
            
    except FileNotFoundError:
        print(f"✗ Помилка: Файл {filename} не знайдено!")
        return False
    except PermissionError:
        print(f"✗ Помилка: Немає дозволу на читання файлу {filename}!")
        return False
    except Exception as e:
        print(f"✗ Неочікувана помилка при читанні файлу: {e}")
        return False
    return True

def process_inflation_data(input_file, output_file, threshold):
    """Обробка даних про інфляцію та пошук значень вище порогу"""
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            csv_reader = csv.reader(infile)
            headers = next(csv_reader)  # Читаємо заголовки
            
            # Знаходимо індекс стовпця з 2016 роком
            try:
                year_2016_index = headers.index("2016")
            except ValueError:
                print("✗ Помилка: Стовпця з даними за 2016 рік не знайдено!")
                return False
            
            # Збираємо дані та фільтруємо
            filtered_data = []
            country_index = headers.index("Country Name") if "Country Name" in headers else 0
            
            for row in csv_reader:
                if len(row) > max(country_index, year_2016_index):
                    country = row[country_index]
                    try:
                        inflation_2016 = float(row[year_2016_index]) if row[year_2016_index] else 0
                        if inflation_2016 > threshold:
                            filtered_data.append(row)
                    except ValueError:
                        # Пропускаємо рядки з некоректними даними
                        continue
            
            # Записуємо результати у новий файл
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                csv_writer = csv.writer(outfile)
                
                # Записуємо заголовки
                csv_writer.writerow(headers)
                
                # Записуємо відфільтровані дані
                for row in filtered_data:
                    csv_writer.writerow(row)
            
            print(f"✓ Знайдено {len(filtered_data)} країн з інфляцією вище {threshold}%")
            print(f"✓ Результати записано у файл: {output_file}")
            return True
            
    except FileNotFoundError:
        print(f"✗ Помилка: Вхідний файл {input_file} не знайдено!")
        return False
    except PermissionError:
        print(f"✗ Помилка: Немає дозволу на читання/запис файлів!")
        return False
    except Exception as e:
        print(f"✗ Неочікувана помилка при обробці даних: {e}")
        return False

def create_sample_csv():
    """Створення тестового CSV файлу з даними про інфляцію (якщо немає реального файлу)"""
    sample_data = [
        ["Country Name", "Country Code", "Indicator Name", "Indicator Code", "2015", "2016", "2017"],
        ["Ukraine", "UKR", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "48.7", "12.4", "14.4"],
        ["United States", "USA", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "0.1", "1.3", "2.1"],
        ["Germany", "DEU", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "0.5", "0.5", "1.5"],
        ["Turkey", "TUR", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "7.7", "7.8", "11.1"],
        ["Argentina", "ARG", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "26.9", "25.7", "25.7"],
        ["Japan", "JPN", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "0.8", "-0.1", "0.5"],
        ["Venezuela", "VEN", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "121.7", "254.9", "438.1"],
        ["Brazil", "BRA", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "9.0", "8.7", "3.4"],
        ["Russia", "RUS", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "15.5", "7.0", "3.7"],
        ["China", "CHN", "Inflation, consumer prices (annual %)", "FP.CPI.TOTL.ZG", "1.4", "2.0", "1.6"]
    ]
    
    try:
        with open('inflation_data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(sample_data)
        print("✓ Тестовий файл 'inflation_data.csv' створено успішно!")
        return True
    except Exception as e:
        print(f"✗ Помилка створення тестового файлу: {e}")
        return False

def main():
    """Головна функція програми"""
    print("=" * 80)
    print("ПРОГРАМА ДЛЯ АНАЛІЗУ ДАНИХ ПРО ІНФЛЯЦІЮ ЗА 2016 РІК")
    print("=" * 80)
    
    input_filename = "inflation_data.csv"
    output_filename = "high_inflation_countries.csv"
    
    # Перевіряємо наявність вхідного файлу, якщо немає - створюємо тестовий
    if not os.path.exists(input_filename):
        print("✗ Вхідний файл не знайдено. Створюємо тестовий файл...")
        if not create_sample_csv():
            return
    
    # Виводимо вміст вихідного файлу
    print("\n1. ВИВІД ВМІСТУ ВИХІДНОГО ФАЙЛУ:")
    if not display_csv_file(input_filename):
        return
    
    # Отримуємо поріг від користувача
    print("\n2. ВВЕДЕННЯ ПОРОГУ ДЛЯ ПОШУКУ:")
    print("-" * 40)
    try:
        threshold = float(input("Введіть поріг інфляції (%): "))
        print(f"Шукаємо країни з інфляцією вище {threshold}% за 2016 рік...")
    except ValueError:
        print("✗ Помилка: Будь ласка, введіть коректне числове значення!")
        return
    
    # Обробляємо дані та створюємо новий файл
    print("\n3. ОБРОБКА ДАНИХ ТА ПОШУК:")
    print("-" * 40)
    if process_inflation_data(input_filename, output_filename, threshold):
        # Виводимо результати
        print("\n4. РЕЗУЛЬТАТИ ПОШУКУ:")
        if not display_csv_file(output_filename):
            print("✗ Файл з результатами створено, але не вдалось його прочитати.")
    else:
        print("✗ Не вдалось обробити дані!")

# Альтернативна спрощена версія
def simple_version():
    """Спрощена версія програми"""
    try:
        # Створюємо тестовий файл якщо потрібно
        if not os.path.exists('inflation.csv'):
            data = [
                ["Country", "2016"],
                ["Ukraine", "12.4"],
                ["USA", "1.3"],
                ["Germany", "0.5"],
                ["Turkey", "7.8"],
                ["Argentina", "25.7"],
                ["Venezuela", "254.9"]
            ]
            with open('inflation.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print("Тестовий файл створено!")
        
        # Виводимо вміст
        print("\nВміст файлу inflation.csv:")
        with open('inflation.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                print(" | ".join(row))
        
        # Отримуємо поріг
        threshold = float(input("\nВведіть поріг інфляції: "))
        
        # Фільтруємо дані
        results = []
        with open('inflation.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                if float(row[1]) > threshold:
                    results.append(row)
        
        # Записуємо результати
        with open('filtered_inflation.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(results)
        
        print(f"\nЗнайдено {len(results)} країн. Результати у filtered_inflation.csv")
        
        # Виводимо результати
        print("\nРезультати пошуку:")
        for country, inflation in results:
            print(f"{country}: {inflation}%")
            
    except FileNotFoundError:
        print("Файл не знайдено!")
    except ValueError:
        print("Некоректне значення порогу!")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
    
    # Для спрощеної версії розкоментуйте:
    # simple_version()