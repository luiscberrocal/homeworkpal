from datetime import timedelta, date
from factory import LazyAttribute, lazy_attribute, SubFactory
from factory.django import DjangoModelFactory
from common.utils import get_fiscal_year
from employee.tests.factories import CompanyGroupFactory, EmployeeFactory
from ..models import Project, ProjectMember, ProjectGoal

__author__ = 'lberrocal'
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class ProjectFactory(DjangoModelFactory):

    class Meta:
        model = Project

    short_name = LazyAttribute(lambda x: faker.sentence(nb_words=6, variable_nb_words=True))
    description =  LazyAttribute(lambda x: faker.paragraphs(nb=2))
    planned_start_date = LazyAttribute(lambda x: faker.date_time_between(start_date="+1m", end_date="+1y"))
    # planned_end_date
    # actual_start_date
    # actual_end_date
    # slug
    planned_man_hours = 1500
    type = 'PROJECT'
    group = SubFactory(CompanyGroupFactory)
    priority = 10

    @lazy_attribute
    def planned_end_date(self):
        return self.planned_start_date + +timedelta(days=180)

    @lazy_attribute
    def fiscal_year(self):
        return get_fiscal_year(self.planned_start_date)


class ProjectMemberFactory(DjangoModelFactory):

    class Meta:
        model = ProjectMember

    role = 'MEMBER'
    employee = SubFactory(EmployeeFactory)
    project = SubFactory(ProjectFactory)


class ProjectGoalFactory(DjangoModelFactory):

    class Meta:
        model = ProjectGoal

    name = LazyAttribute(lambda x: faker.sentence(nb_words=6, variable_nb_words=True))
    description = LazyAttribute(lambda x: faker.paragraphs(nb=2))
    expectations = LazyAttribute(lambda x: faker.paragraphs(nb=1))
    project = None
    employee = SubFactory(EmployeeFactory)
    weight = 0.1

    @lazy_attribute
    def fiscal_year(self):
        if self.project:
            return get_fiscal_year(self.project.planned_start_date)
        else:
            return get_fiscal_year(date.today())

