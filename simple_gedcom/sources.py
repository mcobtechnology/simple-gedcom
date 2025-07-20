from typing import List
from .parser import GedcomParser

def get_source_list(parser: GedcomParser) -> List[dict]:
    """Get all source records as dictionaries"""
    sources_dict = parser.get_sources()
    
    sources_list = []
    for source in sources_dict.values():
        source_data = {
            'Source ID': source.get_pointer(),
            'Title': source.get_title(),
            'Author': source.get_author(),
            'Publication': source.get_publication(),
            'Repository': source.get_repository()
        }
        sources_list.append(source_data)
    
    return sources_list

def get_person_source_list(parser: GedcomParser) -> List[dict]:
    """Get people data with one row per person-source combination"""
    person_source_list = []

    # Go through all individuals
    for person in parser.get_individuals().values():
        pointer = person.get_pointer()
        person_sources = person.get_all_person_sources()

        # Base person data
        base_person_data = {
            'Person ID': pointer
        }

        if person_sources:
            # Create one row per source
            for source_pointer in person_sources:
                sources_dict = parser.get_sources()
                if source_pointer in sources_dict:
                    source = sources_dict[source_pointer]
                    row_data = base_person_data.copy()
                    row_data.update({
                        'Source ID': source.get_pointer(),
                        'Source Title': source.get_title(),
                        'Source Author': source.get_author(),
                        'Source Publication': source.get_publication(),
                        'Source Repository': source.get_repository()
                    })
                    person_source_list.append(row_data)

    return person_source_list