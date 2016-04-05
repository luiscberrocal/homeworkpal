from django.test import TestCase

from jira_git.models import StashRepository
from .factories import StashRepositoryFactory


class TestStashRepository(TestCase):

    def test_create(self):
        repo = StashRepositoryFactory.create()
        db_repo = StashRepository.objects.all()[0]
        self.assertEqual(repo.name, db_repo.name)