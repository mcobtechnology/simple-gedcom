# Simple GEDCOM Parser

A simplified Python library for extracting genealogy data from GEDCOM files, focused on two primary use cases:

1. **Extract basic person data** - Get a clean list of people with vital information and family relationships
2. **Extract person-source relationships** - Map people to their documentary sources

## Features

- Parse GEDCOM 5.5 files
- Extract person data: names, birth/death dates and places, parents
- Extract source citations linked to individuals
- Simple, clean API designed for data analysis
- Easy integration with pandas DataFrames


## Quick Start

```python
from gedcom import GedcomParser
import pandas as pd

# Parse GEDCOM file
parser = GedcomParser()
parser.parse_file('family_tree.ged')

# Get list of all people
people = parser.get_person_list()
people_df = pd.DataFrame(people)

# Get person-source relationships
person_sources = parser.get_person_sources()
sources_df = pd.DataFrame(person_sources)
```

## API Reference

### GedcomParser

#### `parse_file(file_path, strict=False)`
Parse a GEDCOM file.

**Parameters:**
- `file_path` (str): Path to the GEDCOM file
- `strict` (bool): If True, raise exceptions on parse errors

#### `get_person_list()`
Returns a list of dictionaries containing person data:

```python
[
    {
        'Person ID': '@I1@',
        'First Name': 'John',
        'Last Name': 'Doe',
        'Birth Date': '1990',
        'Birth Place': 'New York',
        'Death Date': '',
        'Death Place': '',
        'Father First Name': 'Robert',
        'Father Last Name': 'Doe',
        'Mother First Name': 'Jane',
        'Mother Last Name': 'Smith'
    },
    # ... more people
]
```

#### `get_person_sources()`
Returns a list of dictionaries with person-source relationships:

```python
[
    {
        'Person ID': '@I1@',
        'Source ID': '@S1@',
        'Source Title': 'Birth Certificate',
        'Source Author': '',
        'Source Publication': 'City Records',
        'Source Repository': 'City Hall'
    },
    # ... more person-source combinations
]
```

## Example Usage

### Basic Person Data

```python
from gedcom import GedcomParser

parser = GedcomParser()
parser.parse_file('my_family.ged')

# Get all people
people = parser.get_person_list()

# Print summary
print(f"Found {len(people)} people in the family tree")

# Look at first person
if people:
    person = people[0]
    print(f"Name: {person['First Name']} {person['Last Name']}")
    print(f"Born: {person['Birth Date']} in {person['Birth Place']}")
```

### With Pandas

```python
import pandas as pd
from gedcom import GedcomParser

parser = GedcomParser()
parser.parse_file('my_family.ged')

# Create DataFrames
people_df = pd.DataFrame(parser.get_person_list())
sources_df = pd.DataFrame(parser.get_person_sources())

# Analyze the data
print("Birth places:")
print(people_df['Birth Place'].value_counts())

print("\nSource types:")
print(sources_df['Source Title'].value_counts())
```

## Requirements

- Python 3.6+
- No external dependencies for core functionality
- pandas (optional, for DataFrame examples)

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Attribution

This project is derived from [python-gedcom](https://github.com/nickreynke/python-gedcom) by Nicklas Reincke and contributors. The original project provided the foundation for GEDCOM parsing, which has been simplified and focused for specific genealogy data extraction use cases.

Original Copyright (C) 2018-2019 Nicklas Reincke and contributors  
Simplified version Copyright (C) 2025 [mcobtechnology]

## Contributing

This is a simplified, focused library. If you need additional GEDCOM functionality, consider using the full-featured [python-gedcom](https://github.com/nickreynke/python-gedcom) library.

For bug fixes and improvements to the core functionality, feel free to open issues or submit pull requests.