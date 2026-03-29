from typing import List, Tuple
from functools import cached_property

class GedcomElement:
    """Base class for GEDCOM elements"""

    def __init__(self, level: int, pointer: str, tag: str, value: str):
        self.__level = level
        self.__pointer = pointer
        self.__tag = tag
        self.__value = value
        self.__children = []
        self.__children_by_tag = {}

    def get_level(self) -> int:
        return self.__level

    def get_pointer(self) -> str:
        return self.__pointer

    def get_tag(self) -> str:
        return self.__tag

    def get_value(self) -> str:
        return self.__value

    def get_children(self) -> List['GedcomElement']:
        return self.__children

    def add_child(self, element: 'GedcomElement'):
        self.__children.append(element)
        tag = element.get_tag()
        if tag not in self.__children_by_tag:
            self.__children_by_tag[tag] = []
        self.__children_by_tag[tag].append(element)

    def get_child_elements(self, tag: str = None) -> List['GedcomElement']:
        if tag is None:
            return self.__children
        return self.__children_by_tag.get(tag, [])

    def get_child_value(self, tag: str) -> str:
        """Value of the first child element with a specific tag"""
        elements = self.get_child_elements(tag)
        return elements[0].get_value() if elements else ''


class Person(GedcomElement):
    """Individual person element"""

    @cached_property
    def _name(self) -> Tuple[str, str]:
        name_elements = self.get_child_elements('NAME')
        if not name_elements:
            return ('', '')
        name_value = name_elements[0].get_value()
        if not name_value:
            return ('', '')
        if '/' in name_value:
            parts = name_value.split('/')
            given_names = parts[0].strip()
            surname = parts[1].strip() if len(parts) > 1 else ''
            return (given_names, surname)
        else:
            parts = name_value.strip().split()
            if len(parts) > 1:
                return (' '.join(parts[:-1]), parts[-1])
            elif len(parts) == 1:
                return (parts[0], '')
        return ('', '')

    def get_name(self) -> Tuple[str, str]:
        """Returns (first_name, last_name)"""
        return self._name

    @cached_property
    def _gender(self) -> str:
        return self.get_child_value('SEX')

    def get_gender(self) -> str:
        return self._gender

    @cached_property
    def _birth_date_place(self) -> Tuple[str, str]:
        birth_elements = self.get_child_elements('BIRT')
        if not birth_elements:
            return ('', '')
        birth_element = birth_elements[0]
        return (birth_element.get_child_value('DATE'), birth_element.get_child_value('PLAC'))

    def get_birth_date_place(self) -> Tuple[str, str]:
        return self._birth_date_place

    @cached_property
    def _death_date_place(self) -> Tuple[str, str]:
        death_elements = self.get_child_elements('DEAT')
        if not death_elements:
            return ('', '')
        death_element = death_elements[0]
        return (death_element.get_child_value('DATE'), death_element.get_child_value('PLAC'))

    def get_death_date_place(self) -> Tuple[str, str]:
        return self._death_date_place

    @cached_property
    def _all_person_sources(self) -> List[str]:
        seen = set()
        stack = [self]
        while stack:
            element = stack.pop()
            for source_elem in element.get_child_elements('SOUR'):
                value = source_elem.get_value()
                if value:
                    seen.add(value)
            stack.extend(GedcomElement.get_children(element))
        return list(seen)

    def get_all_person_sources(self) -> List[str]:
        """Get all source pointers associated with this person"""
        return self._all_person_sources


class SourceElement(GedcomElement):
    """Source element"""

    def get_title(self) -> str:
        return self.get_child_value('TITL')

    def get_author(self) -> str:
        return self.get_child_value('AUTH')

    def get_publication(self) -> str:
        return self.get_child_value('PUBL')

    def get_repository(self) -> str:
        return self.get_child_value('REPO')


class FamilyElement(GedcomElement):
    """Family element - minimal implementation for parent lookup"""

    @cached_property
    def _husband(self) -> str:
        return self.get_child_value('HUSB')

    def get_husband(self) -> str:
        return self._husband

    @cached_property
    def _wife(self) -> str:
        return self.get_child_value('WIFE')

    def get_wife(self) -> str:
        return self._wife

    def get_children(self) -> List[str]:
        return [child.get_value() for child in self.get_child_elements('CHIL')]
