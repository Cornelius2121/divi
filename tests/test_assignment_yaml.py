import unittest
import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import AssignmentParams, Person, assignPeople, saveAssignmentYaml, loadAssignmentYamls


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
        saveAssignmentYaml(people, f"{parent_dir}/tests/data/assignments_{params.this_year}_tmp.yaml", params.this_year)

    def test_load_assignments_2021(self):
        year = 2021
        people = loadAssignmentYamls([f"{parent_dir}/tests/data/assignments_{year}.yaml"])

        self.assertEqual(len(people), 4)

        # Tim Smith
        person_tim_smith = [p for p in people if p.getFullName() == "Tim Smith"]
        self.assertEqual(len(person_tim_smith), 1, "Expected to find one person with name Tim Smith")
        person_tim_smith = person_tim_smith[0]
        self.assertEqual(len(person_tim_smith.already_on_prev_keys), 1, "Expected Tim Smith to have bought for only one person")
        hasBoughtForCorny = "Cornelius Spence" in person_tim_smith.already_on_prev_keys
        self.assertTrue(hasBoughtForCorny, "Expected Tim Smith to have bought for Cornelius Spence")

        # Jon Scott
        person_jon_scott = [p for p in people if p.getFullName() == "Jon Scott"]
        self.assertEqual(len(person_jon_scott), 1, "Expected to find one person with name Jon Scott")
        person_jon_scott = person_jon_scott[0]
        self.assertEqual(len(person_jon_scott.already_on_prev_keys), 1, "Expected Jon Scott to have bought for only one person")
        hasBoughtForMacy = "Macy Spence" in person_jon_scott.already_on_prev_keys
        self.assertTrue(hasBoughtForMacy, "Expected Jon Scott to have bought for Macy Spence")

        # Cornelius Spence
        person_cornelius_spence = [p for p in people if p.getFullName() == "Cornelius Spence"]
        self.assertEqual(len(person_cornelius_spence), 1, "Expected to find one person with name Cornelius Spence")
        person_cornelius_spence = person_cornelius_spence[0]
        self.assertEqual(len(person_cornelius_spence.already_on_prev_keys), 1, "Expected Cornelius Spence to have bought for only one person")
        hasBoughtForTim = "Tim Smith" in person_cornelius_spence.already_on_prev_keys
        self.assertTrue(hasBoughtForTim, "Expected Cornelius Spence to have bought for Tim Smith")

        # Macy Spence
        person_macy_spence = [p for p in people if p.getFullName() == "Macy Spence"]
        self.assertEqual(len(person_macy_spence), 1, "Expected to find one person with name Macy Spence")
        person_macy_spence = person_macy_spence[0]
        self.assertEqual(len(person_macy_spence.already_on_prev_keys), 1, "Expected Macy Spence to have bought for only one person")
        hasBoughtForJon = "Jon Scott" in person_macy_spence.already_on_prev_keys
        self.assertTrue(hasBoughtForJon, "Expected Macy Spence to have bought for Jon Scott")


if __name__ == '__main__':
    unittest.main()
