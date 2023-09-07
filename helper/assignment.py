from __future__ import annotations

import math
from typing import List
import numpy as np
# import lapjv
import datetime

this_year = datetime.datetime.now().year


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
        assert other is not self, "Expected other to not be self"
        self.already_on_this_keys.append(other.key())

    def addPersonHasBeenOn(self, other: Person, year: int) -> None:
        assert other is not self, "Expected other to not be self"
        self.already_on_prev_keys.append(other.key())
        self.already_on_prev_year.append(year)

    def getFullName(self) -> str:
        return f"{self.first_name} {self.last_name}"

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


    def __repr__(self) -> str:
        out =  f"{self.getFullName()}"
        if len(self.already_on_this_keys)>0:
            out += f" is buying for " +", ".join(self.already_on_this_keys)
        return out


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
            if person_i == person_j:
                c += params.cost_cant_be_on

            if person_j.isBuyingFor(person_i):
                c += params.cost_of_assignment

            if person_i.hasBoughtForPreviously(person_j):
                years = person_i.yearsBoughtFor(person_j)
                for year in years:
                    c += params.costForYearAssignment(year)
            cost_matrix[i, j] = c
    return cost_matrix


def assignPeople(people: List[Person], params: AssignmentParams) ->  List[Person]:
    cost_matrix = formCostMatrix(people, params)
    raise Exception("LAPJV is not installed")
    # Run Hungarian algorithm
    row_ind, col_ind, _ = lapjv.lapjv(cost_matrix)
    for row in row_ind:
        person = people[row]
        for col in col_ind:
            person.addPersonToBeOn(people[col])
    return people
