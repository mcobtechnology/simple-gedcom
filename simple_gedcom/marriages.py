from typing import List
from .parser import GedcomParser


def get_marriages(parser: GedcomParser) -> List[dict]:
    """Get marriage data with one row per family"""
    individuals = parser.get_individuals()
    marriages = []

    for family in parser.get_families().values():
        husband_id = family.get_husband() or ''
        wife_id = family.get_wife() or ''

        husband = individuals.get(husband_id)
        wife = individuals.get(wife_id)

        husband_first, husband_last = husband.get_name() if husband else ('', '')
        wife_first, wife_last = wife.get_name() if wife else ('', '')
        marriage_date, marriage_place = family.get_marriage_date_place()

        marriages.append({
            'Family ID': family.get_pointer(),
            'Husband ID': husband_id,
            'Husband First Name': husband_first,
            'Husband Last Name': husband_last,
            'Wife ID': wife_id,
            'Wife First Name': wife_first,
            'Wife Last Name': wife_last,
            'Marriage Date': marriage_date,
            'Marriage Place': marriage_place,
        })

    return marriages
