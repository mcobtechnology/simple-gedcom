from typing import List
import pandas as pd
from .parser import GedcomParser

def get_person_list(parser: GedcomParser) -> List[dict]:
    """Get people data with one row per person"""
    person_list = []

    # Go through all individuals
    for person in parser.get_individuals().values():
        pointer = person.get_pointer()
        first_name, last_name = person.get_name()
        birth_date, birth_place = person.get_birth_date_place()
        death_date, death_place = person.get_death_date_place()

        # Get father and mother
        father, mother = parser.get_father_mother(person)
        father_first_name = father_last_name = father_pointer = ''
        mother_first_name = mother_last_name = mother_pointer = ''

        if father:
            father_first_name, father_last_name = father.get_name()
            father_pointer = father.get_pointer()
        if mother:
            mother_first_name, mother_last_name = mother.get_name()
            mother_pointer = mother.get_pointer()

        # Base person data
        person_data = {
            'Person ID': pointer,
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
            'Father ID': father_pointer,
            'Mother ID': mother_pointer
        }

        person_list.append(person_data)

    return person_list

def save_people_to_csv(parser: GedcomParser, output_filename: str = None):
    """Get people data and save to CSV file"""
    import pandas as pd
    import os
    
    # Get the original GEDCOM file path from parser
    gedcom_filepath = parser.get_file_path()
    if gedcom_filepath is None:
        raise ValueError("No GEDCOM file has been parsed yet")
    
    # If no output filename specified, use the GEDCOM file's path and name
    if output_filename is None:
        directory = os.path.dirname(gedcom_filepath)
        base_name = os.path.splitext(os.path.basename(gedcom_filepath))[0]
        output_filename = os.path.join(directory, f"{base_name}.csv")
    
    # Get the people data
    people = get_person_list(parser)
    
    # Convert to DataFrame
    people_df = pd.DataFrame(people)
    
    # Save to CSV
    people_df.to_csv(output_filename, index=False)
    
    return output_filename
