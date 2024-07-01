import psycopg2
import os
import dotenv

dotenv.load_dotenv()


class DBManager:
    def __init__(self, name):
        """
        Инициализация DBManager с указанием имени базы данных.

        :param name: Имя базы данных.
        """
        self.__name = name

    def __execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос к базе данных и возвращает результат.

        :param query: SQL-запрос для выполнения.
        :param params: Параметры для запроса (если есть).
        :return: Результат выполнения запроса.
        """
        conn = psycopg2.connect(dbname=self.__name, user=os.getenv("user"),
                                password=os.getenv("password"), host=os.getenv("host"),
                                port=os.getenv("port"))
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()

        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """
        Возвращает список всех компаний и количество вакансий у каждой компании.

        :return: Список кортежей с именами компаний и количеством вакансий.
        """
        query = """
            SELECT e.name, COUNT(v.id) as vacancies_count
            FROM employers e
            JOIN vacancies v ON e.id = v.employer
            GROUP BY e.name
            ORDER BY vacancies_count DESC
        """
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """
        Возвращает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

        :return: Список кортежей с информацией о вакансиях.
        """
        query = """
            SELECT e.name as company_name, v.name as vacancy_name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer
            ORDER BY v.name
        """
        return self.__execute_query(query)

    def get_avg_salary(self):
        """
        Возвращает среднюю зарплату по вакансиям.

        :return: Средняя зарплата по вакансиям.
        """
        query = """
            SELECT ROUND(AVG((v.salary_from + v.salary_to) / 2.0)::numeric, 2) as avg_salary
            FROM vacancies v
            WHERE v.salary_from > 0 AND v.salary_to > 0
        """
        result = self.__execute_query(query)
        return result[0][0] if result else None

    def get_vacancies_with_higher_salary(self):
        """
        Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

        :return: Список кортежей с информацией о вакансиях.
        """
        query = """
            SELECT e.name as company_name, v.name as vacancy_name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer
            WHERE v.salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from > 0)
            ORDER BY v.name
        """
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """
        Возвращает список всех вакансий, в названии которых содержится указанное ключевое слово.

        :param keyword: Ключевое слово для поиска в названиях вакансий.
        :return: Список кортежей с информацией о вакансиях.
        """
        keyword = f'%{keyword}%'
        query = """
            SELECT e.name as company_name, v.name as vacancy_name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON e.id = v.employer
            WHERE v.name ILIKE %s
            ORDER BY v.name
        """
        return self.__execute_query(query, (keyword,))
