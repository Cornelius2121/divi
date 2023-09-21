import os
import sys
from unittest import TestCase, main

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import Person


class TestFullName(TestCase):
    def test_when_initialised_with_no_last_name(self):
        p = Person("Tim")
        self.assertEqual(p.getFullName(), "Tim")
        self.assertEqual(p.getFirstName(), "Tim")
        self.assertEqual(p.getLastName(), "")

    def test_when_initialised_with_no_last_name_and_trailing_spaces(self):
        p = Person("  Tim  ")
        self.assertEqual(p.getFullName(), "Tim")
        self.assertEqual(p.getFirstName(), "Tim")
        self.assertEqual(p.getLastName(), "")

    def test_when_initialised_with_last_name(self):
        p = Person("Tim", "Smith")
        self.assertEqual(p.getFullName(), "Tim Smith")
        self.assertEqual(p.getFirstName(), "Tim")
        self.assertEqual(p.getLastName(), "Smith")
    def test_when_initialised_with_last_name_and_trailing_spaces(self):
        p = Person(" Tim  ", "  Smith ")
        self.assertEqual(p.getFullName(), "Tim Smith")
        self.assertEqual(p.getFirstName(), "Tim")
        self.assertEqual(p.getLastName(), "Smith")

    def test_when_initialised_with_first_name_and_last_name_together(self):
        p = Person("Tim Smith")
        self.assertEqual(p.getFullName(), "Tim Smith")
        self.assertEqual(p.getFirstName(), "Tim")
        self.assertEqual(p.getLastName(), "Smith")


if __name__ == "__main__":
    main()
