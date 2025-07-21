from typing import List
import pandas as pd
from .parser import GedcomParser
from .elements import Person 

def fill_person(parser: GedcomParser, person: Person) -> dict:
    """Fill person data dictionary"""
    
    first_name, last_name = person.get_name()
    
    birth_date, birth_place = person.get_birth_date_place()
    death_date, death_place = person.get_death_date_place()
    
    return {
        'Person ID': person.get_pointer(),
        'First Name': first_name,
        'Last Name': last_name,
        'Birth Date': birth_date,
        'Birth Place': birth_place,
        'Death Date': death_date,
        'Death Place': death_place
    }

def get_person_list(parser: GedcomParser) -> List[dict]:
    """Get people data with one row per person"""
    person_list = []

    # Go through all individuals
    for person in parser.get_individuals().values():

        person_data = fill_person(parser, person)

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

def get_pedigree(parser: GedcomParser):
         
    root_child_elements = parser.get_root_child_elements()

    pedigree = {}
        
    for element in root_child_elements:
        if isinstance(element, Person):
            # GENERATION 1
            pedigree["HP"] = fill_person(parser, element)

            # GENERATION 2
            parents = parser.get_parents(element)
            
            for parent in parents:
                
                if parent.get_gender() == 'M':
                    pedigree["P1"] = fill_person(parser, parent)
                    # GENERATION 3
                    grandparents = parser.get_parents(parent)
                    
                    for grandparent in grandparents:
                        if grandparent is None:  # Safety check
                            continue
                                                    
                        if grandparent.get_gender() == 'M':
                            pedigree["GP1"] = fill_person(parser, grandparent)
                        else:
                            pedigree["GP2"] = fill_person(parser, grandparent)
                else:
                    # MATERNAL
                    pedigree["P2"] = fill_person(parser, parent)
                    # GENERATION 3
                    grandparents = parser.get_parents(parent)
                    
                    for grandparent in grandparents:
                        
                        if grandparent.get_gender() == 'M':
                            pedigree["GP3"] = fill_person(parser, grandparent)
                        else:
                            pedigree["GP4"] = fill_person(parser, grandparent)

            break
                
    # return the pedigree dictionary
    return pedigree