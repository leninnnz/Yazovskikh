import csv
import re
import os
from prettytable import ALL
from prettytable import PrettyTable

dic_experience = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
                  "moreThan6": "Более 6 лет"}

dic_currency = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро",
                "GEL": "Грузинский лари", "KGS": "Киргизский сом", "KZT": "Тенге",
                "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум"}

dic_bool = {"TRUE": "TRUE", "FALSE": "FALSE", "False": "Нет", "True": "Да"}

reversed_dic_name = {"Название": "name", "Описание": "description", "Навыки": "key_skills",
                     "Опыт работы": "experience_id", "Премиум-вакансия": "premium", "Компания": "employer_name",
                     "Название региона": "area_name", "Дата публикации вакансии": "published_at",
                     "Идентификатор валюты оклада": "salary_currency", "Оклад": "salary"}

reversed_dic_translate = {"Нет опыта": "noExperience", "От 1 года до 3 лет": "between1And3",
                          "От 3 до 6 лет": "between3And6", "Более 6 лет": "moreThan6", "Манаты": "AZN",
                          "Белорусские рубли": "BYR", "Евро": "EUR", "Грузинский лари": "GEL",
                          "Киргизский сом": "KGS", "Тенге": "KZT", "Рубли": "RUR", "Гривны": "UAH",
                          "Доллары": "USD", "Узбекский сум": "UZS", "TRUE": "TRUE", "FALSE": "FALSE",
                          "Нет": "False", "Да": "True"}

currency_to_rub = {"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74,
                   "KGS": 0.76, "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}

experience_to_num = {"noExperience": 0, "between1And3": 1, "between3And6": 2,
                     "moreThan6": 3}


class Salary:
    """
    Класс описывает сущность оклада

    Атрибуты (все атрибуты имеют свойства)
    ------------------------------------------------------------------------
    __salary_from: str
        Нижняя граница оклада
    __salary_to: str
        Верхняя граница оклада
    __salary_currency: str
        Валюта оклада
    __salary_gross: str
        До вычета налогов или нет
    """
    def __init__(self, vacancy_dict: {}):
        """
        Инициализирует объект
        :param vacancy_dict: {str: str}
            Словарь содержащий информацию о вакансии
        """
        self.__salary_from = vacancy_dict["salary_from"]
        self.__salary_to = vacancy_dict["salary_to"]
        self.__salary_gross = vacancy_dict["salary_gross"]
        self.__salary_currency = vacancy_dict["salary_currency"]

    @property
    def salary_from(self) -> str:
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value: str):
        self.__salary_from = value

    @property
    def salary_to(self) -> str:
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, value: str):
        self.__salary_to = value

    @property
    def salary_currency(self) -> str:
        return self.__salary_currency

    @salary_currency.setter
    def salary_currency(self, value: str):
        self.__salary_currency = value

    @property
    def salary_gross(self) -> str:
        return self.__salary_gross

    @salary_gross.setter
    def salary_gross(self, value: str):
        self.__salary_gross = value

    def get_average_ruble_salary(self):
        return (float(self.salary_from) + float(self.salary_to)) / 2 * currency_to_rub[self.salary_currency]


class Vacancy_table:
    """
    Класс описывает сущность вакансии (Вакансии для печать таблицы)

    Атрибуты (все атрибуты имеют свойства)
    ------------------------------------------------------------------------
    __name: str
        Название вакансии
    ___description: str
        Описание вакансии
    __key_skills: [str]
        Список требуемых навыков
    __experience_id: str
        Информация о требуемом опыте работы
    __premium: str
        Премиальная вакансия или нет
    __employer_name: str
        Имя работодателя
    __salary: Salary
        Оклад
    __area_name: str
        Название региона
    __published_at: str
        Дата публикации вакансии
    """
    def __init__(self, vacancy_dict: {}):
        self.__name = vacancy_dict["name"]
        self.__description = vacancy_dict["description"]
        self.__key_skills = vacancy_dict["key_skills"]
        self.__experience_id = vacancy_dict["experience_id"]
        self.__premium = vacancy_dict["premium"]
        self.__employer_name = vacancy_dict["employer_name"]
        self.__salary = Salary(vacancy_dict)
        self.__area_name = vacancy_dict["area_name"]
        self.__published_at = vacancy_dict["published_at"]

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def key_skills(self) -> str:
        return self.__key_skills

    @key_skills.setter
    def key_skills(self, value: str):
        self.__key_skills = value

    @property
    def experience_id(self) -> str:
        return self.__experience_id

    @experience_id.setter
    def experience_id(self, value: str):
        self.__experience_id = value

    @property
    def premium(self) -> str:
        return self.__premium

    @premium.setter
    def premium(self, value: str):
        self.__premium = value

    @property
    def employer_name(self) -> str:
        return self.__employer_name

    @employer_name.setter
    def employer_name(self, value: str):
        self.__employer_name = value

    @property
    def salary(self) -> Salary:
        return self.__salary

    @salary.setter
    def salary(self, value: str):
        self.__salary = value

    @property
    def area_name(self) -> str:
        return self.__area_name

    @area_name.setter
    def area_name(self, value: str):
        self.__area_name = value

    @property
    def published_at(self) -> str:
        return self.__published_at

    @published_at.setter
    def published_at(self, value: str):
        self.__published_at = value


class DataSet_table:
    """
    Класс обеспечивает получение, хранение и обработку данных из CSV файла

     Атрибуты
    ------------------------------------------------------------------------
    file_name: str
        Название CSV файла, в котором содержится вся информация
    vacancies_objects: [Vacancy]
        Список объектов Vacancy содержащих информацию для обработки
    """
    def __init__(self, file_name: str, vacancies: [Vacancy_table] = []):
        """
        Инициализирует объект
        :param file_name: str
            Название CSV файла
        :param vacancies: [Vacancy]
            Список объектов Vacancy содержащих информацию для обработки
        """
        self.file_name = file_name
        self.vacancies_objects = vacancies

    def csv_parser(self):
        """
        Преобразует данные из CSV файла в список вакансий
        :return: [Vacancy] / None
            Список вакансий, если файл не пустой, иначе None
        """
        data_tuple = self.__csv_reader()
        if self.__is_file_correct(data_tuple):
            return self.__csv_filter(data_tuple[1], data_tuple[0])
        return None

    def __is_file_correct(self, data_tuple: ([], [])) -> bool:
        """
        Проверяет файл на корректность (наличие данных)
        :param data_tuple: ([str], [str])
            Данные предстваленные в виде списка заголовков и списка данных
        :return: bool
            True если файл содержит данные, иначе False

        >>> DataSet_table("vacancies.csv", [])._DataSet_table__is_file_correct((["name", "description"], []))
        Нет данных
        False
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__is_file_correct(None)
        Пустой файл
        False
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__is_file_correct((["name", "description"],
        ... ["Programmer", "Create IT products"]))
        True
        """
        if data_tuple is None:
            print("Пустой файл")
            return False
        elif len(data_tuple[1]) == 0:
            print("Нет данных")
            return False
        return True

    def __csv_reader(self):
        """
        Считывает данные из файла и возвращает очищенные данные
        :return: ([str],[str]) / None
            Данные из файла если файл не пустой, иначе / None
        """
        data = []
        if os.stat(self.file_name).st_size == 0:
            return None
        with open(TableStatistics.file_name, "r", encoding="UTF-8-sig") as file:
            file_reader = csv.DictReader(file, delimiter=",")
            headlines_list = list(file_reader.fieldnames)
            headlines_count = len(headlines_list)
            for line in file_reader:
                data.append(self.__parse_line(line, headlines_list, headlines_count))
        return headlines_list, data

    def __parse_line(self, line, headlines_list: [], headlines_count: int) -> []:
        """
        Преобразует одну строку из CSV файла в список содержащий значения полей
        :param line: str
            Строка из CSV файла
        :param headlines_list: [str]
            Список заголовков
        :param headlines_count: int
            Число Заголовков
        :return: [str]
            Возвращает список значений при корректных данных
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__parse_line(
        ... {"name": "NAME", "description": "DESCRIPTION"}, ["name", "description"], 2)
        ['NAME', 'DESCRIPTION']
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__parse_line(
        ... {"name": "NAME", "description": ""}, ["name", "description"], 2)
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__parse_line(
        ... {"name": "NAME", "description": "DESCRIPTION"}, ["name", "description"], 3)
        """
        row = []
        for headline in headlines_list:
            if line[headline] and len(line[headline]) != 0:
                row.append(line[headline])
        if len(row) == headlines_count:
            return row

    def __parse_to_vacance(self, line, headlines_list: []) -> Vacancy_table:
        """
        Преобразует строку в объект Vacancy_table
        :param line: str
            Строка с данными
        :param headlines_list: [str]
            Список заголовков
        :return: Vacancy_table
            Объект содержащий информацию о вакансии

        >>> DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ... ["NAME","DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        ... "AREA_NAME", "200:01:01"],
        ... ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        ... "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]).name
        'NAME'
        >>> len(DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ... ["NAME","DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        ... "AREA_NAME", "200:01:01"],
        ... ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        ... "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]).key_skills)
        1
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ... ["NAME","DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        ... "AREA_NAME", "200:01:01"],
        ... ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        ... "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]).salary.salary_from
        '100'
        """
        vacance = {}
        for i in range(0, len(headlines_list)):
            if headlines_list[i] == "key_skills":
                value_list = line[i].split("\n")
                clean_value_list = list(map(
                    lambda val: self.__remove_white_spaces(self.__remove_HTML_tags(val)), value_list))
                vacance[headlines_list[i]] = clean_value_list
            else:
                vacance[headlines_list[i]] = self.__remove_white_spaces(self.__remove_HTML_tags(line[i]))

        return Vacancy_table(vacance)

    def __remove_HTML_tags(self, string: str) -> str:
        """
        Убирает все HTML теги из строки
        :param string: str
            Исходная строка
        :return: str
            Стррока без HTML тегов
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_HTML_tags("")
        ''
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_HTML_tags("Str without tags")
        'Str without tags'
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_HTML_tags("<p>Str without tags</p>")
        'Str without tags'
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_HTML_tags("<h1><p>Str without tags</p></h1>")
        'Str without tags'
        """
        return re.sub(r'<.*?>', '', string)

    def __remove_white_spaces(self, string: str) -> str:
        """
        Убирает все лишние пробелы
        :param string: str
            Исходная строка
        :return: str
            Строка без лишних пробелов
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_white_spaces(" ")
        ''
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_white_spaces(" String without spaces")
        'String without spaces'
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_white_spaces(" String without spaces ")
        'String without spaces'
        >>> DataSet_table("vacancies.csv", [])._DataSet_table__remove_white_spaces(" String        without  spaces    ")
        'String without spaces'
        """
        #no_undue_spaces = re.sub(r"\s+", " ", string)
        #return no_undue_spaces.replace("\n", "").replace("\r", "").strip()

        #str_without_sym = string.replace("\n", "").replace("\r", "")
        #chars = []
        #was_space = True
        #for c in str_without_sym:
        #    if c == ' ' and was_space:
        #        continue
        #    elif c != ' ':
        #        was_space = False
        #    elif c == ' ' and not was_space:
        #        was_space = True
        #    chars.append(c)
        #return "".join(chars).strip()

        #chars = []
        #was_space = True
        #for c in string:
        #    if (c == ' ' and was_space) or c == '\n' or c == '\r':
        #        continue
        #    elif c != ' ':
        #        was_space = False
        #    elif c == ' ' and not was_space:
        #        was_space = True
        #    chars.append(c)
        #return "".join(chars).strip()

        return " ".join(string.split())


    def __csv_filter(self, data: [], headlines: []) -> []:
        """
        Фильтрует все данные, оставляя только корректные
        :param data: [str]
            Исходные неотфильтрованные данные
        :param headlines: [str]
            Список заголовков
        :return: [Vacancy_table]
            Список вакансий с корректными данными

        >>> len(DataSet_table("vacancies.csv", [])._DataSet_table__csv_filter(
        ... [["NAME","DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        ... "AREA_NAME", "2000:01:01"],
        ... ["NAME","DESCRIPTION", "Python", "lessthan2", "True", "EMPLOYER_NAME", "20", "200", "False", "RUR",
        ... "AREA_NAME", "2001:01:01"]],
        ... ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        ... "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]))
        2
        >>> len(DataSet_table("vacancies.csv", [])._DataSet_table__csv_filter(
        ... [["NAME","DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        ... "AREA_NAME", "2000:01:01"],
        ... ["NAME","DESCRIPTION", "Python", "lessthan2", "True", "EMPLOYER_NAME", "20", "200", "False", "RUR",
        ... "AREA_NAME", "2001:01:01"], None, None],
        ... ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        ... "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]))
        2
        """
        result_vacancies = []
        for line in data:
            if line is not None:
                result_vacancies.append(self.__parse_to_vacance(line, headlines))
        return result_vacancies


class InputConect:
    """
    Класс обеспечивает соединение ввода-вывода данных с пользователем, а также обработку ввода пользователя
    """
    @staticmethod
    def is_input_correct() -> bool:
        """
        Проверяет правильность ввода пользователя
        :return: bool
            True если ввод корректен, иначе False
        """
        if len(TableStatistics.filter_parameter) < 2 and TableStatistics.filter_input != "":
            print("Формат ввода некорректен")
            return False
        elif TableStatistics.filter_input != "" and TableStatistics.filter_parameter[0] not in reversed_dic_name.keys():
            print("Параметр поиска некорректен")
            return False
        elif TableStatistics.sort_parameter != "" and TableStatistics.sort_parameter not in reversed_dic_name.keys():
            print("Параметр сортировки некорректен")
            return False
        elif TableStatistics.is_reverse_sort != "" and TableStatistics.is_reverse_sort != "Да" \
                and TableStatistics.is_reverse_sort != "Нет":
            print("Порядок сортировки задан некорректно")
            return False
        return True

    @staticmethod
    def filter_vacancies(vacancies: [Vacancy_table]):
        """
        Фильтрует вакансии по ранне заданному признаку
        :param vacancies: [Vacancy_table]
            Список вакансий
        :return: [Vacancy_table]
            Отфильтрованный список вакансий
        """
        filter_parameter = TableStatistics.filter_parameter
        if TableStatistics.filter_input == "":
            return vacancies
        if filter_parameter[0] in ["Название", "Название региона", "Компания"]:
            return list(filter(lambda vacance: getattr(vacance,
                                                       reversed_dic_name[filter_parameter[0]]) == filter_parameter[1],
                               vacancies))
        elif filter_parameter[0] in ["Опыт работы", "Премиум-вакансия"]:
            return list(filter(lambda vacance: getattr(vacance,
                                                       reversed_dic_name[filter_parameter[0]]) ==
                                               reversed_dic_translate[filter_parameter[1]], vacancies))
        elif filter_parameter[0] == "Идентификатор валюты оклада":
            return list(filter(lambda vacance:
                               vacance.salary.salary_currency == reversed_dic_translate[filter_parameter[1]],
                               vacancies))
        elif filter_parameter[0] == "Навыки":
            return list(filter(lambda vacance: all(skill in vacance.key_skills
                                                   for skill in list(
                filter(lambda skill: skill != "", filter_parameter[1].split(", ")))), vacancies))
        elif filter_parameter[0] == "Оклад":
            return list(filter(lambda vacance: int(vacance.salary.salary_from) <= int(filter_parameter[1])
                                               <= int(vacance.salary.salary_to), vacancies))
        elif filter_parameter[0] == "Дата публикации вакансии":
            return list(filter(lambda vacance: InputConect.parse_date(
                vacance.published_at) == filter_parameter[1], vacancies))

    @staticmethod
    def sort_vacancies(vacancies: [Vacancy_table]):
        """
        Сортирует список вакансий
        :param vacancies: [Vacancy_table]
            Исходный список вакансий
        :return: [Vacancy_table]
            Отсортированный список вакансий
        """
        sort_parameter = TableStatistics.sort_parameter
        needReverse = True if TableStatistics.is_reverse_sort == "Да" else False
        if sort_parameter == "" or sort_parameter not in reversed_dic_name.keys():
            return vacancies
        if sort_parameter in ["Премиум-вакансия", "Идентификатор валюты оклада",
                              "Название", "Название региона", "Компания"]:
            return list(sorted(vacancies, key=lambda vacance: getattr(vacance, reversed_dic_name[sort_parameter]),
                               reverse=needReverse))
        elif sort_parameter == "Опыт работы":
            return list(sorted(vacancies, key=lambda vacance: experience_to_num[vacance.experience_id],
                               reverse=needReverse))
        elif sort_parameter == "Дата публикации вакансии":
            return list(sorted(vacancies, key=lambda vacance: vacance.published_at, reverse=needReverse))
        elif sort_parameter == "Оклад":
            return list(sorted(vacancies, key=lambda vacance: vacance.salary.get_average_ruble_salary(),
                               reverse=needReverse))
        elif sort_parameter == "Навыки":
            return list(sorted(vacancies, key=lambda vacance: len(vacance.key_skills), reverse=needReverse))

    @staticmethod
    def get_vacancies_table(vacancies: []):
        """
        Создает и возвращает таблицу PrettyTable
        :param vacancies: [Vacancy_table]
            Список вакансий для создания таблицы
        :return: PrettyTable / None
            Возвращает таблицу если есть данные, иначе None
        """
        if vacancies is None:
            return None
        if len(vacancies) == 0:
            print('Ничего не найдено')
            return None

        table = PrettyTable()
        table.field_names = ["№"] + ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
                                     "Оклад", "Название региона", "Дата публикации вакансии"]
        table.align = "l"
        table.hrules = ALL
        table.max_width = 20
        for i, vacance in enumerate(vacancies):
            cutted_values = InputConect.cut_values(list(InputConect.formatter(vacance).values()))
            table.add_row([i + 1] + cutted_values)
        return table

    @staticmethod
    def print_vacancies_table(table: PrettyTable):
        """
        Печатает таблицу с нужными столбцами и строками
        :param table: Таблица для печать
        :return: void
        """
        table.start = TableStatistics.low_confine if TableStatistics.low_confine is not None else 0
        if TableStatistics.high_confine is not None:
            table.end = TableStatistics.high_confine
        correct_fields_names = list(filter(
            lambda name: name != "" and name in table.field_names, TableStatistics.columns_names))
        table.fields = \
            ["№"] + correct_fields_names if len(correct_fields_names) > 0 else table.field_names
        print(table.get_string())

    @staticmethod
    def cut_values(values: []) -> []:
        """
        Обрезает все строки длиннее 100 символов
        :param values: [str]
            Список исходных строк
        :return: [str]
            Список обрезаных строк
        """
        cutted_values = []
        for value in values:
            if len(value) > 100:
                value = value[0:100] + "..."
            cutted_values.append(value)
        return cutted_values

    @staticmethod
    def formatter(vacancy: Vacancy_table) -> {}:
        """
        Форматирует Vacancy_table в словарь для печати правильного отображения во время печати
        :param vacancy: Vacancy_table
            Объект хранящий нформацию о вакансии
        :return: {str: }
            Словарь содержащий информацию о вакансии
        """
        vacance = {}
        vacance["Название"] = vacancy.name if len(vacancy.name) != 0 else "Нет данных"
        vacance["Описание"] = vacancy.description if len(vacancy.description) != 0 else "Нет данных"
        vacance["Навыки"] = "\n".join(vacancy.key_skills) if vacancy.key_skills[0] != "" else "Нет данных"
        vacance["Опыт работы"] = dic_experience[vacancy.experience_id] if len(
            vacancy.experience_id) != 0 else "Нет данных"
        vacance["Премиум-вакансия"] = dic_bool[vacancy.premium] if len(vacancy.premium) != 0 else "Нет данных"
        vacance["Компания"] = vacancy.employer_name if len(vacancy.employer_name) != 0 else "Нет данных"
        vacance["Оклад"] = InputConect.parse_salary_field(vacancy.salary)
        vacance["Название региона"] = vacancy.area_name if len(vacancy.area_name) != 0 else "Нет данных"
        vacance["Дата публикации вакансии"] = \
            InputConect.parse_date(vacancy.published_at) if len(vacancy.published_at) != 0 else "Нет данных"
        return vacance

    @staticmethod
    def parse_salary_field(salary: Salary) -> str:
        """
        Преобразует Salary в строковое поле для удобного отображения
        :param salary: Salary
            Объект содержащий информацию о окладе
        :return: str
            Строковое представление Salary
        """
        if len(salary.salary_from) == 0 or len(salary.salary_to) == 0 \
                or len(salary.salary_gross) == 0 or len(salary.salary_currency) == 0:
            return "Нет данных"
        gross = "Без вычета налогов" if salary.salary_gross == "True" else "С вычетом налогов"
        return f"{InputConect.parse_salary(salary.salary_from, salary.salary_to)}" \
               f" ({dic_currency[salary.salary_currency]}) ({gross})"

    @staticmethod
    def parse_salary(low: str, high: str) -> str:
        """
        Преобразует величину оклада
        :param low: str
            Нижняя граница оклада
        :param high: str
            Верхняя граница оклада
        :return: str
            Преобразованная строка
        """
        low_str = str(int(low.split(".")[0]))
        high_str = str(int(high.split(".")[0]))
        if len(low_str) <= 3 or len(high_str) <= 3:
            return f"{low_str.strip()} - {high_str.strip()}"
        return f"{low_str[0:-3].strip()} {low_str[-3:].strip()} - {high_str[0:-3].strip()} {high_str[-3:].strip()}"

    @staticmethod
    def parse_date(date_str: str) -> str:
        """
        Преобразует строку даты
        :param date_str: str
            Исходная строка
        :return: str
            Преобразованная строка
        """
        year = date_str[0:4]
        month = date_str[5:7]
        day = date_str[8:10]
        return f"{day}.{month}.{year}"


class TableStatistics:
    """
    Класс реализующий логику запроса данных у пользователя и вывода таблицы о вакансиях
    """
    @staticmethod
    def start_table_programm():
        """
        Запрашивает всю информацию у пользователя и печатает таблицу о вакансиях
        :return: void
        """
        TableStatistics.file_name = input("Введите название файла: ")
        TableStatistics.filter_input = input("Введите параметр фильтрации: ")
        TableStatistics.filter_parameter = list(filter(lambda item: item != "", TableStatistics.filter_input.split(": ")))
        TableStatistics.sort_parameter = input("Введите параметр сортировки: ")
        TableStatistics.is_reverse_sort = input("Обратный порядок сортировки (Да / Нет): ")
        confines = list(filter(lambda confine_str: confine_str != "", input("Введите диапазон вывода: ").split(" ")))
        TableStatistics.columns_names = input("Введите требуемые столбцы: ").split(", ")

        TableStatistics.low_confine = int(confines[0]) - 1 if len(confines) > 0 else None
        TableStatistics.high_confine = int(confines[1]) - 1 if len(confines) > 1 else None

        if InputConect.is_input_correct():
            dataset = DataSet_table(TableStatistics.file_name)
            dataset.vacancies_objects = dataset.csv_parser()
            if dataset is not None:
                vacancies_table = InputConect.get_vacancies_table(
                    InputConect.sort_vacancies(InputConect.filter_vacancies(dataset.vacancies_objects)))
                if vacancies_table is not None:
                    InputConect.print_vacancies_table(vacancies_table)

#import doctest
#doctest.testfile("Table_statistics.py")