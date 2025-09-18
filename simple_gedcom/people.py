from typing import List
from .parser import GedcomParser
from .elements import Person 
from .utils import save_data_to_csv

def fill_person(parser: GedcomParser, person: Person) -> dict:
    """Fill person data dictionary"""
    
    first_name, last_name = person.get_name()
    
    birth_date, birth_place = person.get_birth_date_place()
    death_date, death_place = person.get_death_date_place()
    
    # Get parents
    father, mother = parser.get_father_mother(person)

    father_first_name = father_last_name = father_id = ""
    mother_first_name = mother_last_name = mother_id = ""

    if father:
        father_first_name, father_last_name = father.get_name()
        father_id = father.get_pointer()

    if mother:
        mother_first_name, mother_last_name = mother.get_name()
        mother_id = mother.get_pointer()

    # Populate dictionary    
    return {
        'First Name': first_name,
        'Last Name': last_name,
        'Birth Date': birth_date,
        'Birth Place': birth_place,
        'Death Date': death_date,
        'Death Place': death_place,
        'Father First Name': father_first_name,
        'Father Last Name': father_last_name,
        'Mother First Name': mother_first_name,
        'Mother Last Name': mother_last_name,
        'Person ID': person.get_pointer(),
        'Father ID': father_id,
        'Mother ID': mother_id
    }

def get_person_list(parser: GedcomParser) -> List[dict]:
    """Get people data with one row per person"""
    person_list = []

    # Go through all individuals
    for person in parser.get_individuals().values():

        person_data = fill_person(parser, person)

        person_list.append(person_data)

    return person_list

def find_persons_by_name(parser: GedcomParser, first_name: str = None, last_name: str = None) -> list:
    """Find persons by first and/or last name"""
    if first_name is None and last_name is None:
        # If no search criteria provided, return all persons
        return get_person_list(parser)
    
    person_list = get_person_list(parser)
    matched_persons = []
    
    for person in person_list:
        match = True
        
        # Check first name if provided
        if first_name is not None:
            person_first_name = person.get('First Name', '').strip()
            if first_name.lower() not in person_first_name.lower():
                match = False
        
        # Check last name if provided
        if last_name is not None:
            person_last_name = person.get('Last Name', '').strip()
            if last_name.lower() not in person_last_name.lower():
                match = False
        
        if match:
            matched_persons.append(person)
    
    return matched_persons

def save_person_list_to_csv(parser: GedcomParser, output_filename: str = None) -> str:
    """Get people data and save to CSV file"""
    person_list = get_person_list(parser)
    return save_data_to_csv(parser, person_list, " people", output_filename)

