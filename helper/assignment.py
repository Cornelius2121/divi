from __future__ import annotations

import datetime
import math
import os.path
from typing import List, Tuple

import numpy as np
import scipy
import pathlib as Path

import yaml


def join_string_with_commas(
        strings: List[str], joiner="and", oxford_comma=False
) -> str:
    str_out = strings[0]
    if len(strings) > 2:
        str_out = ", ".join(strings[0:-1])
        if oxford_comma:
            str_out += ","
    if len(strings) > 1:
        str_out += f" {joiner} " + strings[-1]
    return str_out


class Person:
    def __init__(self, first_name: str, last_name: str = "") -> None:
        first_name = first_name.strip()
        last_name = last_name.strip()
        names = first_name.split(" ")
        if len(names) == 1:
            self.first_name = first_name
            self.last_name = last_name
        elif len(names) == 2:
            if len(last_name) > 0:
                raise ValueError("Expected last_name to empty when first name has two names!")
            self.first_name = names[0]
            self.last_name = names[1]
        else:
            raise ValueError("Expected first_name argument to have one or two names!")

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
        assert (
                other is not self
        ), f"Expected {other.getFullName()} to not be {self.getFullName()}"
        self.already_on_this_keys.append(other.key())

    def addPersonHasBeenOn(self, other: Person, year: int) -> None:
        assert (
                other is not self
        ), f"Expected {other.getFullName()} to not be {self.getFullName()}"
        self.already_on_prev_keys.append(other.key())
        self.already_on_prev_year.append(year)

    def getFullName(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def getFirstName(self) -> str:
        return self.first_name

    def getLastName(self) -> str:
        return self.last_name

    def hasBoughtForPreviously(self, other: Person) -> bool:
        return other.key() in self.already_on_prev_keys

    def yearsBoughtFor(self, other: Person) -> List[int]:
        assert self.hasBoughtForPreviously(
            other
        ), f"Expected to have bought for {other.getFullName()} previously"
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
            names = join_string_with_commas(self.already_on_this_keys)
            out += f" is buying for {names}"
        else:
            out += " is not buying for anyone"
        return out

    def toDict(self, only_save_this_year=True) -> dict:
        d = dict()
        d["first_name"] = self.first_name
        d["last_name"] = self.last_name
        d["already_on_this_keys"] = self.already_on_this_keys
        if not only_save_this_year:
            d["keys_that_cant_be_on"] = self.keys_that_cant_be_on
            d["already_on_prev_year"] = self.already_on_prev_year
            d["already_on_prev_keys"] = self.already_on_prev_keys

        return d

    @staticmethod
    def fromDict(data: dict, additional_keys_to_assign: List[str] = None) -> Person:
        p = Person(data["first_name"], data["last_name"])
        if additional_keys_to_assign is not None:
            for key in additional_keys_to_assign:
                if key in data:
                    setattr(p, key, data[key])
        return p

    def __str__(self):
        return self.__repr__()


class AssignmentParams:
    def __init__(
            self, years_of_not_repeating: int, this_year: int = datetime.datetime.now().year
    ) -> None:
        self.cost_cant_be_on = 10000
        self.cost_of_assignment = 1
        self.cost_of_double_assignment = 100
        self.years_of_not_repeating = years_of_not_repeating
        self.this_year = this_year

    def costForYearAssignment(self, year_previous: int) -> float:
        assert (
                year_previous < self.this_year
        ), f"Expected year_previous ({year_previous}) to be less than this year ({self.this_year})"
        delta = self.this_year - year_previous
        return self.cost_of_double_assignment * math.exp(
            -delta / self.years_of_not_repeating
        )


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


def saveAssignmentYaml(people: List[Person], file_name: Path, year: int) -> None:
    dict_out = dict()
    npersons = len(people)
    ndigits = int(math.log10(npersons)) + 1

    for i, person in enumerate(people):
        label = f"person_{i:{ndigits}}"
        dict_out[label] = person.toDict()
    dict_out["year"] = year
    with open(file_name, "w") as f:
        yaml.dump(dict_out, f)



def loadAssignmentYamls(file_names: List[Path]) -> List[Person]:
    if not isinstance(file_names, list):
        raise ValueError(f"Expected file_names to be a list, got {type(file_names)}")
    people = []
    for file_name in file_names:
        if not os.path.isfile(file_name):
            raise ValueError(f"Expected {file_name} to exist!")

    # Get names of all people in all files
    for file_name in file_names:
        with open(file_name, "r") as f:
            dict_in = yaml.load(f, Loader=yaml.FullLoader)
            for key, data in dict_in.items():
                if key != "year":
                    person = Person.fromDict(data)
                    people.append(person)

    # Merge duplicates
    keys = [p.key() for p in people]
    unique_keys = list(set(keys))
    unique_people = []
    for key in unique_keys:
        people_with_key = [p for p in people if p.key() == key]
        assert len(people_with_key) > 0, f"Expected to find people with key {key}"
        if len(people_with_key) > 1:
            print(f"Found duplicate people with key {key}")
            people_with_key = [people_with_key[0]]
        unique_people.append(people_with_key[0])

    for file_name in file_names:
        with open(file_name, "r") as f:
            dict_in = yaml.load(f, Loader=yaml.FullLoader)
            year = dict_in["year"]
            for key, data in dict_in.items():
                if key != "year":
                    temp_person = Person.fromDict(data)
                    person = [p for p in unique_people if p.key() == temp_person.key()][0]
                    if "already_on_this_keys" in data:
                        for key in data["already_on_this_keys"]:
                            person.addPersonHasBeenOn(
                                [p for p in unique_people if p.key() == key][0], year
                            )
    return unique_people

