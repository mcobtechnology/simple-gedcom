import unittest
from simple_gedcom import GedcomParser, get_person_list, get_person_source_list

class TestGedcomParser(unittest.TestCase):
    
    def test_parser_creation(self):
        """Test that parser can be created"""
        parser = GedcomParser()
        self.assertIsNotNone(parser)
    
    def test_empty_person_list(self):
        """Test parser with no file returns empty list"""
        parser = GedcomParser()
        people = get_person_list(parser)  # Fixed
        self.assertEqual(len(people), 0)
    
    def test_empty_sources_list(self):
        """Test parser with no file returns empty sources"""
        parser = GedcomParser()
        sources = get_person_source_list(parser)  # Fixed
        self.assertEqual(len(sources), 0)

    def test_real_gedcom_file(self):
        """Test parser with actual GEDCOM file"""
        parser = GedcomParser()
        
        # Parse the test file
        parser.parse_file('tests/data/tree.ged')
        
        # Get people and verify we found some
        people = get_person_list(parser)  # Fixed
        self.assertGreater(len(people), 0, "Should find at least one person")
        
        # Check that first person has expected structure
        if people:
            person = people[0]
            self.assertIn('Person ID', person)
            self.assertIn('First Name', person)
            self.assertIn('Last Name', person)
        
        # Test sources
        sources = get_person_source_list(parser)  # Fixed
        print(f"Found {len(people)} people and {len(sources)} sources")

if __name__ == '__main__':
    unittest.main()