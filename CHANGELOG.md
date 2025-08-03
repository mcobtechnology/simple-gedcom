# Changelog

## [1.0.4] - 2025-08-03
### Changed
- Change project name to use an underscore instead of a hyphen
- to comply with the latest PEP standards

## [1.0.3] - 2025-08-02
### Added
- Added pedigree functions

### Changed
- Allow simpler calling without instantiating the parser object

## [1.0.2] - 2025-07-28
### Added
- Add unit tests
- Add toml file to supplement setup.py

## [1.0.0] - 2025-07-14
### Added
- Complete rewrite as simplified GEDCOM parser
- `get_person_list()` method for extracting basic person data
- `get_person_sources()` method for person-source relationships
- Streamlined API focused on two main use cases

### Changed
- Simplified from full GEDCOM library to focused data extraction tool
- New class structure with cleaner API

### Note
This version is a complete rewrite derived from the original python-gedcom library.