import os

from django.test import TestCase

from common.utils import filename_with_datetime
from homeworkpal_project.settings.base import TEST_OUTPUT_PATH
from project_admin.tests.factories import ProjectSupportFactory
from ..excel import ProjectAdminExcel


class TestProjectAdminExcel(TestCase):

    def test_export(self):
        excel = ProjectAdminExcel()
        filename = filename_with_datetime(TEST_OUTPUT_PATH,'support_export.xlsx')
        supports = ProjectSupportFactory.create_batch(20)
        excel.export_supports(filename, supports)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
        self.assertFalse(os.path.exists(filename))