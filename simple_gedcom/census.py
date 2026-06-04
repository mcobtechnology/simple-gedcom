import re
from typing import List
from .parser import GedcomParser

_RELATION_RE = re.compile(r'Relationships? to Head(?: of House)?\s*:\s*([^;]+)', re.IGNORECASE)


def _parse_relation(note: str) -> str:
    m = _RELATION_RE.search(note)
    return m.group(1).strip() if m else ''


def get_residence_list(parser: GedcomParser) -> List[dict]:
    """Get all RESI events, one row per event per person"""
    sources_dict = parser.get_sources()
    rows = []
    for person in parser.get_individuals().values():
        records = person.get_residence_records()
        if not records:
            continue
        first_name, last_name = person.get_name()
        for date, place, source_pointer, note in records:
            source = sources_dict.get(source_pointer)
            rows.append({
                'Person ID': person.get_pointer(),
                'First Name': first_name,
                'Last Name': last_name,
                'Date': date,
                'Place': place,
                'Source ID': source_pointer,
                'Source Title': source.get_title() if source else '',
                'Relation to Head': _parse_relation(note),
            })
    return rows


def get_census_list(parser: GedcomParser) -> List[dict]:
    """Get RESI events where the source title contains 'census'"""
    return [
        row for row in get_residence_list(parser)
        if 'census' in row['Source Title'].lower()
    ]
