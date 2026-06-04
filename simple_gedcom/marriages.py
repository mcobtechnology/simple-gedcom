import re
from collections import defaultdict
from typing import Dict, List
from .parser import GedcomParser

_MONTH_MAP = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}
_YEAR_RE  = re.compile(r'\b(\d{4})\b')
_MONTH_RE = re.compile(r'\b([a-z]{3,5}\.?)\b', re.IGNORECASE)


def _gedcom_date_sort_key(date_str: str) -> tuple:
    """Return (year, month, day) for sorting; (9999, 99, 99) for empty/unparseable."""
    if not date_str or not date_str.strip():
        return (9999, 99, 99)
    s = date_str.strip()
    year_m = _YEAR_RE.search(s)
    year   = int(year_m.group(1)) if year_m else 9999
    month  = 99
    month_m = _MONTH_RE.search(s)
    if month_m:
        month = _MONTH_MAP.get(month_m.group(1).lower().rstrip('.'), 99)
    day = 99
    if year_m:
        remainder = s[:year_m.start()] + s[year_m.end():]
        day_m = re.search(r'\b(\d{1,2})\b', remainder)
        if day_m:
            day = int(day_m.group(1))
    return (year, month, day)


def _build_spouse_families_index(parser: GedcomParser) -> Dict[str, list]:
    """Map each person pointer → list of families where they are a spouse."""
    index: Dict[str, list] = defaultdict(list)
    for family in parser.get_families().values():
        if family.get_husband():
            index[family.get_husband()].append(family)
        if family.get_wife():
            index[family.get_wife()].append(family)
    return dict(index)


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


def get_marriages_by_person(parser: GedcomParser) -> List[dict]:
    """Get spouse/marriage columns keyed by person — one row per person."""
    spouse_families = _build_spouse_families_index(parser)
    individuals = parser.get_individuals()
    rows = []
    max_marriages = 0

    for person_id, person in individuals.items():
        marriages = []
        for family in spouse_families.get(person_id, []):
            spouse_id = family.get_wife() if family.get_husband() == person_id else family.get_husband()
            spouse = individuals.get(spouse_id)
            s_first, s_last = spouse.get_name() if spouse else ('', '')
            date, _ = family.get_marriage_date_place()
            marriages.append((date, s_first, s_last, family.get_pointer()))

        marriages.sort(key=lambda m: (_gedcom_date_sort_key(m[0]), m[2].lower(), m[1].lower()))

        row = {'Person ID': person_id}
        for n, (date, s_first, s_last, fam_id) in enumerate(marriages, 1):
            row[f'Spouse {n} First Name'] = s_first
            row[f'Spouse {n} Last Name']  = s_last
            row[f'Marriage {n} Date']     = date
            row[f'Family {n} ID']         = fam_id

        max_marriages = max(max_marriages, len(marriages))
        rows.append(row)

    for row in rows:
        for n in range(1, max_marriages + 1):
            row.setdefault(f'Spouse {n} First Name', '')
            row.setdefault(f'Spouse {n} Last Name',  '')
            row.setdefault(f'Marriage {n} Date',     '')
            row.setdefault(f'Family {n} ID',         '')

    return rows
