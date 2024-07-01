import requests


class HHParser:
    """
    Класс для вывода данных с сайта hh.ru (HeadHunter).
    """

    def __get_request(self, url, params):
        """
        Выполняет GET-запрос по-указанному URL с переданными параметрами.

        :param url: URL для запроса.
        :param params: Параметры запроса.
        :return: Ответ в формате JSON, если статус код 200, иначе None.
        """
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def get_employers(self):
        """
        Получает список работодателей с сайта hh.ru.

        :return: Список словарей с информацией о работодателях (id и name).
        """
        params = {"per_page": 10, "sort_by": "by_vacancies_open"}
        data = self.__get_request("https://api.hh.ru/employers", params)
        employers = []
        if data:
            for employer in data["items"]:
                employers.append({"id": employer["id"], "name": employer["name"]})
        return employers

    def __get_vacancies(self, employer_id):
        """
        Получает список вакансий для указанного работодателя.

        :param employer_id: ID работодателя.
        :return: Список вакансий для данного работодателя.
        """
        vacancies = []
        page = 0
        per_page = 100
        while True:
            params = {"employer_id": employer_id, "per_page": per_page, "page": page}
            data = self.__get_request("https://api.hh.ru/vacancies", params)
            if not data or not data["items"]:
                break
            vacancies.extend(data["items"])
            page += 1
        return vacancies

    def get_all_vacancies(self):
        """
        Получает список всех вакансий для всех работодателей.

        :return: Список всех вакансий с деталями (id, name, url, salary_from, salary_to, employer, area).
        """
        employers = self.get_employers()
        all_vacancies = []
        for employer in employers:
            vacancies = self.__get_vacancies(employer["id"])
            for vacancy in vacancies:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] else 0
                all_vacancies.append({
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "url": vacancy["alternate_url"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "employer": employer["id"],
                    "area": vacancy["area"]["name"]
                })
        return all_vacancies
