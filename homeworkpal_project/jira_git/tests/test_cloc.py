from django.test import TestCase

from jira_git.cloc import LinesOfCodeCounter


class TestLinesOfCodeCounter(TestCase):

    def test_count(self):
        code_path = r'C:\Users\lberrocal\Documents\codigo_tino_ns\scientific_application_framework_2'
        cloc = LinesOfCodeCounter(code_path)
        results = cloc.count()
        self.assertTrue(len(results) > 900)