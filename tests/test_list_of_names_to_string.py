from unittest import TestCase
import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import list_of_names_to_string


class Test(TestCase):
    def test_one_name(self):
        names = ['Tim Smith']
        self.assertEqual(list_of_names_to_string(names), 'Tim Smith')

    def test_two_names(self):
        names = ['Tim Smith', 'Jon Scott']
        self.assertEqual(list_of_names_to_string(names), 'Tim Smith and Jon Scott')

    def test_three_names(self):
        names = ['Tim Smith', 'Jon Scott', "Jarvis Jones"]
        self.assertEqual(list_of_names_to_string(names), 'Tim Smith, Jon Scott, and Jarvis Jones')

