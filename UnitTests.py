import unittest
from Table_statistics import DataSet_table
from Table_statistics import Vacancy_table

class Tests_DataSet_table_methods(unittest.TestCase):
    def test_is_file_correct_without_data(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__is_file_correct((["name", "description"], []))
        self.assertEqual(result, False)

    def test_is_file_correct_without_file(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__is_file_correct(None)
        self.assertEqual(result, False)
    def test_is_file_correct_correct_input(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__is_file_correct((["name", "description"],
                                                           ["Programmer", "Create IT products"]))
        self.assertEqual(result, True)

    def test_parse_line_correct_input(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__parse_line({"name": "NAME", "description": "DESCRIPTION"},
                                                     ["name", "description"], 2)
        self.assertEqual(result, ['NAME', 'DESCRIPTION'])

    def test_parse_line_without_value(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__parse_line({"name": "NAME", "description": ""}, ["name", "description"], 2)
        self.assertEqual(result, None)

    def test_parse_line_with_over_headlines(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__parse_line({"name": "NAME", "description": "DESCRIPTION"},
                                                     ["name", "description"], 3)
        self.assertEqual(result, None)

    def test_parse_to_vacance_test_vacance(self):
        test_vacance = DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ["NAME", "DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        "AREA_NAME", "200:01:01"],
        ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"])
        self.assertEqual(test_vacance.name, 'NAME')

    def test_parse_to_vacance_test_key_skills(self):
        test_vacance = DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ["NAME", "DESCRIPTION", "Python\nHTML", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        "AREA_NAME", "200:01:01"],
        ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"])
        self.assertEqual(len(test_vacance.key_skills), 2)

    def test_parse_to_vacance_test_salary(self):
        test_vacance = DataSet_table("vacancies.csv", [])._DataSet_table__parse_to_vacance(
        ["NAME", "DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        "AREA_NAME", "200:01:01"],
        ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"])
        self.assertEqual(test_vacance.salary.salary_from, '100')

    def test_remove_HTML_tags_Empty_string(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_HTML_tags("")
        self.assertEqual(result, '')

    def test_remove_HTML_tags_Empty_string_without_tags(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_HTML_tags("Str without tags")
        self.assertEqual(result, 'Str without tags')

    def test_remove_HTML_tags_Empty_string_with_tags(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_HTML_tags("<p>Str without tags</p>")
        self.assertEqual(result, 'Str without tags')

    def test_remove_HTML_tags_Empty_string_with_inner_tags(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_HTML_tags("<h1><p>Str without tags</p></h1>")
        self.assertEqual(result, 'Str without tags')

    def test_remove_white_spaces_string_only_space(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_white_spaces(" ")
        self.assertEqual(result, '')

    def test_remove_white_spaces_string_left_space(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_white_spaces(" String without spaces")
        self.assertEqual(result, 'String without spaces')

    def test_remove_white_spaces_string_both_spaces(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_white_spaces(" String without spaces ")
        self.assertEqual(result, 'String without spaces')

    def test_remove_white_spaces_string_inner_spaces(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_white_spaces(" String        without  spaces    ")
        self.assertEqual(result, 'String without spaces')

    def test_remove_white_spaces_string_sym(self):
        testData = DataSet_table("vacancies.csv", [])
        result = testData._DataSet_table__remove_white_spaces(" String\n without spaces    ")
        self.assertEqual(result, 'String without spaces')

    def test_csv_filter_without_None(self):
        result = len(DataSet_table("vacancies.csv", [])._DataSet_table__csv_filter(
        [["NAME", "DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        "AREA_NAME", "2000:01:01"],
        ["NAME", "DESCRIPTION", "Python", "lessthan2", "True", "EMPLOYER_NAME", "20", "200", "False", "RUR",
        "AREA_NAME", "2001:01:01"]],
        ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]))
        self.assertEqual(result, 2)

    def test_csv_filter_with_None(self):
        result = len(DataSet_table("vacancies.csv", [])._DataSet_table__csv_filter(
        [["NAME", "DESCRIPTION", "Python", "morethan6", "True", "EMPLOYER_NAME", "100", "2000", "True", "RUR",
        "AREA_NAME", "2000:01:01"],
        ["NAME", "DESCRIPTION", "Python", "lessthan2", "True", "EMPLOYER_NAME", "20", "200", "False", "RUR",
        "AREA_NAME", "2001:01:01"], None, None],
        ["name", "description", "key_skills", "experience_id", "premium", "employer_name",
        "salary_from", "salary_to", "salary_gross", "salary_currency", "area_name", "published_at"]))
        self.assertEqual(result, 2)