from DataSet_class import DataSet
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
import matplotlib.pyplot as plt
import matplotlib
from jinja2 import Environment, FileSystemLoader
import pdfkit
import openpyxl

border = Border(left=Side(border_style='thin', color='FF000000'),
                right=Side(border_style='thin', color='FF000000'),
                top=Side(border_style='thin', color='FF000000'),
                bottom=Side(border_style='thin', color='FF000000'),)

font = Font(bold=True)


class Report:
    """
    Класс для вывода всей полученной статистики в разных форматах

    Атрибуты
    ------------------------------------------------------------------------
    __border: Border
        Объект для хранения стиля границ ячеек в таблице Excel
    __headline_font: Font
        Объект для хранения тиля шрифта для ечеек в таблице Excel
    """
    def __init__(self, border: Border = border, font: Font = font):
        """
        Инициализирует объект
        :param border:
            Стиль для границ
        :param font:
            Стилья для шрифта
        """
        self.__border = border
        self.__headline_font = font

    def generate_excel(self, data: DataSet, salaries_by_town: {str: float}, rates_by_town: {str: float}, current_vacancy_name: str):
        """
        Генерирует Excel файл со всеми готовыми листами и таблицами составленными из данных
        :param data: DataSet
            Данные для создания таблиц
        :param salaries_by_town: {str: float}
            Дополнительные данные для создания таблиц(отобранные и отсортированные)
            Распределение зарплат по городам (ТОП-10)
        :param rates_by_town:{str: float}
            Дополнительные данные для создания таблиц(отобранные и отсортированные)
            Доли вакансий по городам (ТОП-10)
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :return: void
        """
        wb = Workbook()
        years_sheet = wb.active
        self.__fill_year_sheet(years_sheet, data, current_vacancy_name)

        town_sheet = wb.create_sheet("Статистика по городам")
        self.__fill_town_sheet(town_sheet, salaries_by_town, rates_by_town)

        for column in ["A", "B", "C", "D", "E"]:
            years_sheet.column_dimensions[column].width =\
                max(list(map(lambda cell: len(str(cell.value)), years_sheet[column]))) + 2
            town_sheet.column_dimensions[column].width = \
                max(list(map(lambda cell: len(str(cell.value)), town_sheet[column]))) + 2

        wb.save("report.xlsx")

    def __fill_year_sheet(self, sheet, data, current_vacancy_name):
        """
        Заполняет лист данными о распределении по годам
        :param sheet: Sheet
            Лист, в котором создаются таблицы
        :param data: DataSet
            Данные для заполнения
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :return: void
        """
        sheet.title = "Статистика по годам"
        sheet.append(["Год", "Средняя зарплата", "Средняя зарплата - " + current_vacancy_name,
                      "Количество вакансий", "Количество вакансий - " + current_vacancy_name])

        for year in data.salaries_by_year.keys():
            sheet.append([year, data.salaries_by_year[year], data.current_salaries_by_year[year],
                          data.vacancies_count_by_year[year], data.current_count_by_year[year]])

        for row in sheet:
            for cell in row:
                if cell.row == 1:
                    cell.font = self.__headline_font
                cell.border = self.__border

    def __fill_town_sheet(self, sheet, salaries_by_town: {str: float}, rates_by_town: {str: float}):
        """
        Заполняет лист данными о распределении по городам
        :param sheet: Sheet
            Лист, в котором создаются таблицы
        :param salaries_by_town: {str: float}
            Словарь с данными о распределении зарплат по городам
        :param rates_by_town: {str: float}
            Словарь с данными о распределении долей вакансий по городам
        :return: void
        """
        sheet.append(["Город", "Уровень зарплат", " ", "Город", "Доля вакансий"])

        town_rows = []
        for town_item in salaries_by_town.items():
            town_rows.append([town_item[0], town_item[1], " "])

        for i, town_item in enumerate(rates_by_town.items()):
            town_rows[i] += [town_item[0], town_item[1]]
            sheet.append(town_rows[i])

        for row in sheet:
            for cell in row:
                if cell.column == 3:
                    continue
                if cell.row == 1:
                    cell.font = self.__headline_font
                cell.border = self.__border
                if cell.column == 5:
                    cell.number_format = FORMAT_PERCENTAGE_00

    def generate_image(self, data:DataSet, salaries_by_town: {str: float},
                       rates_by_town: {str: float}, current_vacancy_name: str):
        """
        Генерирует png изображение с графиками построенными на основе данных
        :param data: DataSet
            Данные для создания графиков
        :param salaries_by_town: {str: float}
            Дополнительные данные для создания графиков(отобранные и отсортированные)
            Распределение зарплат по городам (ТОП-10)
        :param rates_by_town:{str: float}
            Дополнительные данные для создания графиков(отобранные и отсортированные)
            Доли вакансий по городам (ТОП-10)
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :return: void
        """
        matplotlib.rc('xtick', labelsize=8)
        matplotlib.rc('xtick', labelsize=8)
        plt.figure(figsize=(100, 100))
        fig, axs = plt.subplots(2, 2)

        self.__generate_salary_by_year_graph(data, axs[0, 0],current_vacancy_name)
        self.__generate_count_by_year_graph(data, axs[0, 1], current_vacancy_name)
        self.__generate_salary_by_town_graph(salaries_by_town, axs)
        self.__generate_rates_by_town_graph(rates_by_town, axs)

        fig.tight_layout()
        fig.savefig('graph.png')

    def generate_cut_image(self, data: DataSet) -> str:
        """
        Генерирует png изображение с графиками построенными на основе данных
        :param data: DataSet
            Данные для создания графиков
        :return: str
            Название файла, в который был сохранен график
        """
        matplotlib.rc('xtick', labelsize=8)
        matplotlib.rc('xtick', labelsize=8)
        plt.figure(figsize=(100, 100))
        fig, axs = plt.subplots(2)

        self.__generate_salary_by_year_graph(data, axs[0], data.current)
        self.__generate_count_by_year_graph(data, axs[1], data.current)

        file_name = 'cut_graph.png'
        fig.tight_layout()
        fig.savefig(file_name)
        return  file_name

    def __generate_salary_by_year_graph(self, data: DataSet, ax, current_vacancy_name: str):
        """
        Создает график показывающий динамику зарплат по годам
        :param data: DataSet
            Данные для создания графика
        :param axs: [axis]
            Массив отдельных графиков на одной фигуре
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :return: void
        """
        x = list(map(lambda year: int(year), data.salaries_by_year.keys()))
        ax.bar(list(map(lambda c: c - 0.35, x)), data.salaries_by_year.values(), width=0.35, label="средняя з/п")
        ax.bar(x, data.current_salaries_by_year.values(), width=0.35, label="з/п " + current_vacancy_name)
        ax.set_title('Уровень зарплат по годам')
        ax.set_xticks(x, data.salaries_by_year.keys(), rotation=90, fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(axis='y')

    def __generate_count_by_year_graph(self, data: DataSet, ax, current_vacancy_name: str):
        """
        Создает график показывающий динамику количества вакансий по годам
        :param data: DataSet
            Данные для создания графика
        :param axs: [axis]
            Массив отдельных графиков на одной фигуре
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :return: void
        """
        x = list(map(lambda year: int(year), data.vacancies_count_by_year.keys()))
        ax.bar(list(map(lambda c: c - 0.35, x)), data.vacancies_count_by_year.values(),
                      width=0.35, label="Количество вакансий")
        ax.bar(x, data.current_count_by_year.values(),
                      width=0.35, label="Количество вакансий " + current_vacancy_name)
        ax.set_title('Количество вакансий по годам')
        ax.set_xticks(x, data.vacancies_count_by_year.keys(), rotation=90, fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(axis='y')

    def __generate_salary_by_town_graph(self, salaries_by_town: {str: float}, axs):
        """
        Создает график распределения зарплат по городам
        :param salaries_by_town: {str: float}
            Распределение зарплат по городам (ТОП-10)
        :param axs: [axis]
            Массив отдельных графиков на одной фигуре
        :return: void
        """
        x = list(map(lambda town: town.replace(" ", "\n").replace("-", "-\n"), salaries_by_town.keys()))
        axs[1, 0].barh(x, salaries_by_town.values(), align='center')
        axs[1, 0].set_title('Уровень зарплат по городам')
        axs[1, 0].set_yticks(range(10))
        axs[1, 0].set_yticklabels(x, fontsize=6)
        axs[1, 0].grid(axis='x')
        axs[1, 0].invert_yaxis()

    def __generate_rates_by_town_graph(self, rates_by_town: {str: float}, axs):
        """
        Создает график показывающий доли вакансий в разных городах
        :param rates_by_town: {str: float}
            Доли вакансий по городам (ТОП-10)
        :param axs: [axis]
            Массив отдельных графиков на одной фигуре
        :return: void
        """
        values = [1 - sum(rates_by_town.values())] + list(rates_by_town.values())
        labels = ["Другие"] + list(rates_by_town.keys())
        params_tuple = axs[1, 1].pie(values, labels=labels)
        axs[1, 1].set_title('Доля вакансий по городам')
        [_.set_fontsize(6) for _ in params_tuple[1]]

    def generate_pdf(self, current_vacancy_name: str, image_file: str, tables_file: str):
        """
        Генерирует отчет в виде PDF файла используя готовые файлы графиков и таблиц
        :param current_vacancy_name: str
            Название интересующей нас профессии
        :param image_file: str
            Название png файла с графиками
        :param tables_file: str
            Название Excel файла с таблицами
        :return: void
        """
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("pdf_template.html")

        xfile = openpyxl.load_workbook(tables_file)
        years_headlines, years_values, towns_salaries_headlines,\
            towns_rates_headlines, towns_salaries_values, towns_rates_values = [], [], [], [], [], []

        years_table = xfile["Статистика по годам"]
        years_headlines = years_table[1]
        years_values = [row for row in years_table if row != years_table[1]]

        self.__fill_towns_table(xfile, towns_salaries_headlines, towns_rates_headlines,
                                towns_salaries_values, towns_rates_values)

        pdf_template = template.render({'vacancy_name': current_vacancy_name, 'image_file': image_file,
                                        'years_headlines': years_headlines, 'years_values': years_values,
                                        'towns_salaries_headlines': towns_salaries_headlines,
                                        'towns_salaries_values': towns_salaries_values,
                                        'towns_rates_headlines': towns_rates_headlines,
                                        'towns_rates_values': towns_rates_values})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        options = {'enable-local-file-access': None}
        pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options=options)

    def generate_cut_pdf(self, data: DataSet, image_file: str):
        """
        Генерирует отчет в виде PDF файла используя готовые файлы графиков
        :param data: DataSet
            Датасет с всей информацией
        :param image_file: str
            Название png файла с графиками
        :return: void
        """
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("cut_pdf_template.html")

        years_headlines, years_values = [], []

        years_headlines = ['Год', 'Средняя зарплата', f'Средняя зарплата - {data.current}', 'Количество вакансий',
                           f'Количество вакансий {data.current}']
        for year in data.salaries_by_year.keys():
            years_values.append([year, data.salaries_by_year[year], data.current_salaries_by_year[year],
                                 data.vacancies_count_by_year[year], data.current_count_by_year[year]])
            print(years_values[-1])

        pdf_template = template.render({'vacancy_name': data.current, 'image_file': image_file,
                                        'years_headlines': years_headlines, 'years_values': years_values})
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        options = {'enable-local-file-access': None}
        pdfkit.from_string(pdf_template, 'cut_report.pdf', configuration=config, options=options)

    def __fill_towns_table(self, xfile, towns_salaries_headlines: [str],
                           towns_rates_headlines: [str], towns_salaries_values: [float], towns_rates_values: [float]):
        """
        Заполняет таблицу данными для вставки в html шаблон
        :param xfile: WorkBook
            Открытый Excel WorkBook для получения данных из ячеек
        :param towns_salaries_headlines: [str]
            Список заголовков для таблицы распределения зарплат по городам
        :param towns_rates_headlines: [str]
            Список заколовков для таблицы долей по городам
        :param towns_salaries_values: [float]
            Список значений для таблицы распределения зарплат по городам
        :param towns_rates_values: [float]
            Список значений для таблицы долей по городам
        :return: void
        """
        town_table = xfile["Статистика по городам"]
        for row in town_table:
            salaries_value_row = []
            rates_value_row = []
            for cell in row:
                if cell.row == 1:
                    if cell.column == 1 or cell.column == 2:
                        towns_salaries_headlines.append(cell)
                    elif cell.column == 4 or cell.column == 5:
                        towns_rates_headlines.append(cell)
                else:
                    if cell.column == 1 or cell.column == 2:
                        salaries_value_row.append(cell)
                    elif cell.column == 4 or cell.column == 5:
                        rates_value_row.append(cell)
            if len(salaries_value_row) != 0:
                towns_salaries_values.append(salaries_value_row)
            if len(rates_value_row) != 0:
                towns_rates_values.append(rates_value_row)
