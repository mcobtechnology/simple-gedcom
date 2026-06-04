# tests/test_simple_gedcom.py
import pytest
import os
import tempfile
from simple_gedcom import load_gedcom

def test_load_gedcom():
    """Test that we can load the sample GEDCOM file"""
    gedcom = load_gedcom('tests/data/tree.ged')
    assert gedcom is not None

def test_load_nonexistent_file():
    """Test error handling for missing files"""
    with pytest.raises(FileNotFoundError):
        load_gedcom('does_not_exist.ged')

def test_csv_exports():
    """Test all CSV export functions work without errors"""
    gedcom = load_gedcom('tests/data/tree.ged')

    # simple tests that the functions do not crash
    gedcom.save_person_list_to_csv()
    gedcom.save_person_list_to_csv(extended=True)
    gedcom.save_person_list_to_csv(marriages=True)
    gedcom.save_person_list_to_csv(extended=True, marriages=True)
    gedcom.save_pedigree_to_csv()
    gedcom.save_source_list_to_csv()
    gedcom.save_person_source_list_to_csv()


def test_get_person_list_basic():
    gedcom = load_gedcom('tests/data/tree.ged')
    people = gedcom.get_person_list()
    assert len(people) > 0
    row = people[0]
    assert 'First Name' in row
    assert 'Last Name' in row
    assert 'Person ID' in row
    assert 'Suffix' not in row
    assert 'Gender' not in row
    keys = list(row.keys())
    assert keys[-3:] == ['Person ID', 'Father ID', 'Mother ID']


def test_get_person_list_extended():
    gedcom = load_gedcom('tests/data/tree.ged')
    people = gedcom.get_person_list(extended=True)
    assert len(people) > 0
    row = people[0]
    assert 'Suffix' in row
    assert 'Gender' in row
    assert 'Status' in row
    # ID columns should be at the end
    keys = list(row.keys())
    assert keys[-3:] == ['Person ID', 'Father ID', 'Mother ID']


def test_get_person_list_with_marriages():
    gedcom = load_gedcom('tests/data/tree.ged')
    people = gedcom.get_person_list(marriages=True)
    assert len(people) > 0
    assert 'Suffix' not in people[0]
    assert 'Family 1 ID' in people[0]


def test_get_person_list_extended_and_marriages():
    gedcom = load_gedcom('tests/data/tree.ged')
    people = gedcom.get_person_list(extended=True, marriages=True)
    assert len(people) > 0
    row = people[0]
    assert 'Gender' in row
    keys = list(row.keys())
    # Person ID, Father ID, Mother ID come before marriage columns
    mother_id_pos = keys.index('Mother ID')
    assert keys[mother_id_pos - 2] == 'Person ID'
    assert keys[mother_id_pos - 1] == 'Father ID'
    assert 'Spouse 1 First Name' in keys
    assert keys.index('Spouse 1 First Name') > mother_id_pos