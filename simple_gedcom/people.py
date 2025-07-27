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

def get_pedigree(parser: GedcomParser) -> dict:
    root_child_elements = parser.get_root_child_elements()
    pedigree = {}
    
    for element in root_child_elements:
        if isinstance(element, Person):
            # Start with the root person (HP = Home Person)
            hp_data = fill_person(parser, element)
            hp_data['Generation'] = 1
            pedigree["HP"] = hp_data
            
            # Recursively build the pedigree
            build_pedigree_recursive(parser, element, 1, 1, 10, pedigree)
            break
    
    return pedigree

def build_pedigree_recursive(parser: GedcomParser, person: Person, position_number: int, generation: int, max_generations: int, pedigree: dict):
    """Recursively build pedigree up to max_generations"""
    
    # Stop if we've reached the maximum generation
    if generation > max_generations:
        return
    
    # Get father and mother
    father, mother = parser.get_father_mother(person)
    
    # Calculate positions for next generation (binary tree numbering)
    father_position = position_number * 2
    mother_position = position_number * 2 + 1
    
    # Generate the position keys based on generation
    father_key = get_position_key(father_position, generation)
    mother_key = get_position_key(mother_position, generation)
    
    # Process father
    if father is not None:
        father_data = fill_person(parser, father)
        father_data['Generation'] = generation + 1
        pedigree[father_key] = father_data
        build_pedigree_recursive(parser, father, father_position, generation + 1, max_generations, pedigree)
    
    # Process mother
    if mother is not None:
        mother_data = fill_person(parser, mother)
        mother_data['Generation'] = generation + 1
        pedigree[mother_key] = mother_data
        build_pedigree_recursive(parser, mother, mother_position, generation + 1, max_generations, pedigree)

def get_position_key(position_number: int, generation: int) -> str:
    """Generate position key based on generation and position number"""
    if generation == 1:  # Parents
        return "P1" if position_number == 2 else "P2"
    elif generation == 2:  # Grandparents
        # Position 4,5,6,7 -> GP1,GP2,GP3,GP4
        return f"GP{position_number - 3}"
    else:  # Great-grandparents and beyond
        # Generate G prefix (G, GG, GGG, etc.)
        g_count = generation - 2
        g_prefix = "G" * g_count
        
        # Calculate the starting position for this generation
        # Gen 3: starts at position 8, Gen 4: starts at position 16, etc.
        generation_start = 2 ** generation
        relative_position = position_number - generation_start + 1
        
        return f"{g_prefix}GP{relative_position}"

def save_people_to_csv(parser: GedcomParser, output_filename: str = None) -> str:
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

def save_pedigree_to_csv(parser: GedcomParser, output_filename: str = None) -> str:
    """Get pedigree data and save to CSV file"""
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
        output_filename = os.path.join(directory, f"{base_name}_pedigree.csv")
    
    # Get the pedigree data
    pedigree = get_pedigree(parser)
    
    # Convert to DataFrame
    pedigree_df = pd.DataFrame(pedigree).T.reset_index()

    # Add generation indicators
    pedigree_df.rename(columns={'index': 'Position'}, inplace=True)
    pedigree_df = pedigree_df.sort_values('Generation')

    # Save to CSV
    pedigree_df.to_csv(output_filename, index=False)
    
    return output_filename
