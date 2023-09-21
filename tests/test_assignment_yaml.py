import unittest
import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import AssignmentParams, Person, assignPeople, saveAssignmentYaml


class TestSaveToYaml(unittest.TestCase):
    def test_can_save_as_yaml(self):
        params = AssignmentParams(1, this_year=2021)
        p1 = Person("Tim", "Smith")
        p2 = Person("Jon", "Scott")
        p3 = Person("Cornelius", "Spence")
        p4 = Person("Macy", "Spence")
        p1.addPersonHasBeenOn(p2, 2020)
        p2.addPersonHasBeenOn(p3, 2019)
        p3.addPersonHasBeenOn(p1, 2018)
        p4.addPersonHasBeenOn(p1, 2019)
        p3.addPersonThatCantBeOn(p4)
        p4.addPersonThatCantBeOn(p3)
        people = [p1, p2, p3, p4]

        people = assignPeople(people=people, params=params)
        saveAssignmentYaml(people, f"{parent_dir}/tests/data/assignments_{params.this_year}.yaml", params.this_year)


if __name__ == '__main__':
    unittest.main()
