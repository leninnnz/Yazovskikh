from DataSet_class import DataSet
from Report_class import Report
from Table_statistics import TableStatistics


file_name = input("Введите название файла: ")
current_vacancy_name = input("Введите название профессии: ")

data_set = DataSet(current_vacancy_name)
dates = data_set.currency_frequency_reader(file_name)
data_set.generate_currency(dates[0], dates[1])
vacancies_data = data_set.get_vacancies_data()
data_set.fill_dictionaries(vacancies_data)
data_set.calculate_vacancies_count()
data_set.fill_statistics_dictionaries()

data_set.print_statistics_dictionaries()

