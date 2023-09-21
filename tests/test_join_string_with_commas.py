import os
import sys
from unittest import TestCase

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper.assignment import join_string_with_commas


class Test(TestCase):
    def test_one_name(self):
        names = ['Tim Smith']
        self.assertEqual(join_string_with_commas(names), 'Tim Smith')

    def test_two_names(self):
        names = ['Tim Smith', 'Jon Scott']
        self.assertEqual(join_string_with_commas(names), 'Tim Smith and Jon Scott')

    def test_two_names_oxford(self):
        names = ['Tim Smith', 'Jon Scott']
        self.assertEqual(join_string_with_commas(names, oxford_comma=True), 'Tim Smith and Jon Scott')

    def test_three_names(self):
        names = ['Tim Smith', 'Jon Scott', "Jarvis Jones"]
        self.assertEqual(join_string_with_commas(names), 'Tim Smith, Jon Scott and Jarvis Jones')

    def test_three_names_oxford(self):
        names = ['Tim Smith', 'Jon Scott', "Jarvis Jones"]
        self.assertEqual(join_string_with_commas(names, oxford_comma=True), 'Tim Smith, Jon Scott, and Jarvis Jones')

