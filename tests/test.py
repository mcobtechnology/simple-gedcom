from simple_gedcom import GedcomParser, get_person_list, save_people_to_csv
from simple_gedcom import get_source_list, get_person_source_list, get_pedigree

import pandas as pd

parser = GedcomParser()

parser.parse_file('data/Family Tree.ged')

# person_list = get_person_list(parser)
# df = pd.DataFrame(person_list)
# print(df.head())

# save_people_to_csv(parser)

# pd.set_option('display.max_colwidth', 100)  # or None for no limit

# df_people = pd.DataFrame(get_person_list(parser))
# df_sources = pd.DataFrame(get_person_source_list(parser))

pedigree = get_pedigree(parser)

df = pd.DataFrame(pedigree)

print(df)
