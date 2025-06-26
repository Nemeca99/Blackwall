# BlackwallV2 Project Reorganization

This README documents the reorganization of the BlackwallV2 (Lyra) system implementation files to improve organization and reduce clutter.

## New Folder Structure

### `/batch`
Contains all batch (.bat) files organized by function.

### `/demo`
Contains all demonstration scripts and benchmark programs.

### `/docs`
Documentation is now organized into subject-specific folders:
- `/docs/media` - Media integration documentation
- `/docs/optimization` - System optimization documentation
- `/docs/integration` - Component integration documentation
- `/docs/development` - General development guides and documentation

### `/copilot`
The copilot directory has been reorganized:
- Main journal: `copilots_journal.md`
- `/copilot/journal_entries` - Archive of all journal entry files with timestamps
- `/copilot/journal_index.md` - Index to all journal entries

## Organization Scripts

The following scripts in the `/scripts` directory were used to perform the reorganization:

- `move_batch_files.py` - Moved all batch files to the `/batch` directory
- `organize_documentation.py` - Organized documentation files into categories
- `move_demo_files.py` - Moved standalone demo files to the `/demo` directory
- `organize_journals_new.py` - Organized copilot journal entries

## Original Structure Preserved

The reorganization preserves the original file structure for core system components:

- `/integration` - Integration components
- `/media` - Media processing components
- `/monitoring` - System monitoring dashboard
- `/test` - Test scripts and utilities
- `/tools` - Development and utility tools

## Next Steps

The system organization can be further improved by:

1. Consolidating similar demo files into common scripts with parameters
2. Updating batch files to reference new file locations
3. Creating a unified documentation index
4. Reorganizing the `/test` directory by component
