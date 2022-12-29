from DataSet_class import DataSet
from Report_class import Report
from Table_statistics import TableStatistics


current_vacancy_name = input("Введите название профессии: ")


data_set = DataSet(current_vacancy_name)

data_set.load_data_from_hh()


