from DataSet_class import DataSet
from Report_class import Report
from Table_statistics import TableStatistics


file_name = input("Введите название файла: ")
current_vacancy_name = input("Введите название профессии: ")

data_set = DataSet(current_vacancy_name)
dates = data_set.currency_frequency_reader(file_name='vacancies_dif_currencies.csv')
data_set.generate_currency(dates[0], dates[1])
