from __future__ import annotations

import math
from typing import List
import numpy as np
import scipy
import datetime


def list_of_names_to_string(names: List[str]) -> str:
    nnames = len(names)
    if nnames == 1:
        return names[0]
    elif nnames == 2:
        return f"{names[0]} and {names[1]}"
    elif nnames > 2:
        return ", ".join(names[:-1]) + f", and {names[-1]}"


class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

        self.keys_that_cant_be_on = []
        self.already_on_this_keys = []
        self.already_on_prev_year = []
        self.already_on_prev_keys = []

    def __eq__(self, other: Person) -> bool:
        return self.key() == other.key()

    def key(self) -> str:
        return self.getFullName()

    def addPersonThatCantBeOn(self, other: Person) -> None:
        self.keys_that_cant_be_on.append(other.key())

    def addPersonToBeOn(self, other: Person) -> None:
        assert other is not self, f"Expected {other.getFullName()} to not be {self.getFullName()}"
        self.already_on_this_keys.append(other.key())

    def addPersonHasBeenOn(self, other: Person, year: int) -> None:
        assert other is not self, f"Expected {other.getFullName()} to not be {self.getFullName()}"
        self.already_on_prev_keys.append(other.key())
        self.already_on_prev_year.append(year)

    def getFullName(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def hasBoughtForPreviously(self, other: Person) -> bool:
        return other.key() in self.already_on_prev_keys

    def yearsBoughtFor(self, other: Person) -> int:
        assert self.hasBoughtForPreviously(other), f"Expected to have bought for {other.getFullName()} previously"
        years = []
        for i in range(len(self.already_on_prev_keys)):
            if self.already_on_prev_keys[i] == other.key():
                years.append(self.already_on_prev_year[i])

        return years

    def isBuyingFor(self, other: Person) -> bool:
        return other.key() in self.already_on_this_keys

    def cannotBuyFor(self, other: Person) -> bool:
        return other.key() in self.keys_that_cant_be_on

    def __repr__(self) -> str:
        out = f"{self.getFullName()}"
        if len(self.already_on_this_keys) > 0:
            names = list_of_names_to_string(self.already_on_this_keys)
            out += f" is buying for " + names
        else:
            out += f" is not buying for anyone"
        return out

    def __str__(self):
        return self.__repr__()


class AssignmentParams:
    def __init__(self, years_of_not_repeating: int, this_year: int = datetime.datetime.now().year) -> None:
        self.cost_cant_be_on = 10000
        self.cost_of_assignment = 1
        self.cost_of_double_assignment = 100
        self.years_of_not_repeating = years_of_not_repeating
        self.this_year = this_year

    def costForYearAssignment(self, year_previous: int) -> float:
        assert year_previous < self.this_year, f"Expected year_previous ({year_previous}) to be less than this year ({self.this_year})"
        delta = self.this_year - year_previous
        return self.cost_of_double_assignment * math.exp(- delta / self.years_of_not_repeating)


def formCostMatrix(people: List[Person], params: AssignmentParams) -> np.ndarray:
    num_people = len(people)
    cost_matrix = np.zeros((num_people, num_people))
    for i in range(num_people):
        person_i = people[i]
        for j in range(num_people):
            c = 0
            person_j = people[j]
            if person_i.cannotBuyFor(person_j) or person_j == person_i:
                c += params.cost_cant_be_on

            if person_j.isBuyingFor(person_i):
                c += params.cost_of_assignment

            if person_i.hasBoughtForPreviously(person_j):
                years = person_i.yearsBoughtFor(person_j)
                for year in years:
                    c += params.costForYearAssignment(year)
            cost_matrix[i, j] = c
    return cost_matrix


def assignPeople(people: List[Person], params: AssignmentParams) -> List[Person]:
    cost_matrix = formCostMatrix(people, params)
    # Run Hungarian algorithm

    row_ind, col_ind = scipy.optimize.linear_sum_assignment(cost_matrix)
    for i in row_ind:
        row = row_ind[i]
        col = col_ind[i]
        person = people[row]
        person.addPersonToBeOn(people[col])
    return people
