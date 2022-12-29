from DataSet_class import DataSet
from Report_class import Report
from Table_statistics import TableStatistics

if __name__ == "__main__":
    file_name = input("Введите название файла: ")
    current_vacancy_name = input("Введите название профессии: ")
    current_region = input("Введите название региона: ")

    data_set = DataSet(current_vacancy_name, current_region)
    dates = data_set.currency_frequency_reader(file_name='vacancies_dif_currencies.csv')
    data_set.generate_currency(dates[1], dates[0])
    data_set.get_vacancies_data()
    #data_set.fill_dictionaries_by_pandas()
    #report = Report()
    #img_name = report.generate_town_image(data_set)
    #report.generate_town_pdf(data_set, img_name)

