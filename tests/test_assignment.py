import os
import sys
from unittest import TestCase, main

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import AssignmentParams, Person, assignPeople


class Test(TestCase):
    def test_not_buying_for_self(self):
        params = AssignmentParams(1, this_year=2021)
        p1 = Person("Tim", "Smith")
        p2 = Person("Jon", "Scott")

        people = [p1, p2]

        people = assignPeople(people=people, params=params)

        self.assertTrue(p1.isBuyingFor(p2))
        self.assertTrue(p2.isBuyingFor(p1))

    def test_not_buying_for_people_that_cant_be_on(self):
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

        self.assertFalse(p3.isBuyingFor(p4))
        self.assertFalse(p4.isBuyingFor(p3))


if __name__ == "__main__":
    main()
