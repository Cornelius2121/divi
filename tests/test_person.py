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


class TestToAndFromDict(TestCase):
    def test_when_writing_to_dict(self):
        p = Person("Tim", "Smith")
        p.already_on_prev_keys = ["a", "b", "c"]
        p.already_on_prev_year = [2020, 2021, 2022]
        p.already_on_this_keys = ["d", "e", "f"]
        p.keys_that_cant_be_on = ["g", "h", "i"]

        d = p.toDict(only_save_this_year=False)
        self.assertEqual(d["first_name"], "Tim")
        self.assertEqual(d["last_name"], "Smith")
        self.assertEqual(d["already_on_prev_keys"], ["a", "b", "c"])
        self.assertEqual(d["already_on_prev_year"], [2020, 2021, 2022])
        self.assertEqual(d["already_on_this_keys"], ["d", "e", "f"])

    def test_when_reading_from_dict(self):
        d = dict()
        d["first_name"] = "Tim"
        d["last_name"] = "Smith"
        d["already_on_prev_keys"] = ["a", "b", "c"]
        d["already_on_prev_year"] = [2020, 2021, 2022]
        d["already_on_this_keys"] = ["d", "e", "f"]
        d["keys_that_cant_be_on"] = ["g", "h", "i"]
        person = Person.fromDict(d, only_save_this_year=False)
        self.assertEqual(person.getFullName(), "Tim Smith")
        self.assertEqual(person.already_on_prev_keys, ["a", "b", "c"])
        self.assertEqual(person.already_on_prev_year, [2020, 2021, 2022])
        self.assertEqual(person.already_on_this_keys, ["d", "e", "f"])
        self.assertEqual(person.keys_that_cant_be_on, ["g", "h", "i"])


if __name__ == "__main__":
    main()
