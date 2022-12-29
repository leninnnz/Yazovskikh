# from DataSet_class import DataSet
# from Report_class import Report
# from Table_statistics import TableStatistics
#
#
# if __name__ == "__main__":
#     userQuery = input("Введите команду: (Вакансии / Статистика)")
#     if userQuery == "Вакансии":
#         TableStatistics.start_table_programm()
#     elif userQuery == "Статистика":
#         folder_name = input("Введите название папки: ")
#         file_name = input("Введите название файла: ")
#         current_vacancy_name = input("Введите название профессии: ")
#
#         data_set = DataSet(current_vacancy_name)
#         print(data_set.currency_frequency_reader(file_name='vacancies_dif_currencies.csv'))
#         data_set.generate_currency('2005-09-16T17:26:39+0400', '2022-07-18T19:35:13+0300')
#         file_names = data.csv_split_generator(file_name, folder_name)
#         data.multi_proc_fill_dictionaries(file_names)
#         data.concurrent_futures_fill_dictionaries(file_names)
#         data.fill_dictionaries(DataSet.csv_reader(file_name), current_vacancy_name)
#         data.calculate_vacancies_count()
#         data.fill_statistics_dictionaries()
#
#         data.print_statistics_dictionaries()
#
#         sorted_salaries_by_town = dict(sorted(data.salaries_by_town.items(), key=lambda item: item[1], reverse=True)[0:10])
#         sorted_vacancies_by_rate = dict(sorted(data.vacancies_rate_by_town.items(),
#                                               key=lambda item: item[1], reverse=True)[0:10])
#
#         report = Report()
#         report.generate_excel(data, sorted_salaries_by_town, sorted_vacancies_by_rate, current_vacancy_name)
#         report.generate_image(data, sorted_salaries_by_town, sorted_vacancies_by_rate, current_vacancy_name)
#         report.generate_pdf(current_vacancy_name, "graph.png", "report.xlsx")
#     else:
#         print("Неизвестная команда. Введите 'Вакансии' или 'Статистика'")
