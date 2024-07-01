from src.db_manager import DBManager
from src.utils import create_database, create_tables, insert_tables, delete_database


def user_interface():
    """
    Основная функция для управления базой данных вакансий и компаний.
    Позволяет пользователю взаимодействовать с базой данных через консольный интерфейс.
    """
    db_name = input("Введите название базы данных:")
    print("Ожидайте")
    create_database(db_name)
    create_tables(db_name)
    insert_tables(db_name)
    db_manager = DBManager(db_name)

    while True:
        print("\nВыберите запрос либо введите слово 'Стоп':")
        print("1 - Список всех компаний и количество вакансий у каждой компании")
        print("2 - Список всех вакансий с указанием названия компании,"
              " названия вакансии и зарплаты и ссылки на вакансию")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово")

        choice = input("Ваш выбор: ").strip()

        if choice == 'Стоп':
            print("Работа завершена.")
            break

        try:
            choice = int(choice)
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер запроса.")
            continue

        if choice == 1:
            result = db_manager.get_companies_and_vacancies_count()
            print("\nСписок всех компаний и количество вакансий у каждой компании:")
            for row in result:
                print(f"{row[0]}: {row[1]} вакансий")

        elif choice == 2:
            result = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for row in result:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, "
                      f"Зарплата от: {row[2]}, Зарплата до: {row[3]}, Ссылка: {row[4]}")

        elif choice == 3:
            avg_salary = db_manager.get_avg_salary()
            if avg_salary:
                print(f"\nСредняя зарплата по вакансиям: {avg_salary}")
            else:
                print("\nНет данных о средней зарплате.")

        elif choice == 4:
            result = db_manager.get_vacancies_with_higher_salary()
            print("\nСписок всех вакансий с зарплатой выше средней:")
            for row in result:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, "
                      f"Зарплата от: {row[2]}, Зарплата до: {row[3]}, Ссылка: {row[4]}")

        elif choice == 5:
            keyword = input("Введите ключевое слово для поиска вакансий: ").strip()
            result = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nСписок всех вакансий с ключевым словом '{keyword}':")
            for row in result:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, "
                      f"Зарплата от: {row[2]}, Зарплата до: {row[3]}, Ссылка: {row[4]}")

        else:
            print("Неверный номер запроса. Пожалуйста, выберите существующий номер запроса"
                  " или введите 'Стоп' для завершения.")

    delete_database(db_name)
