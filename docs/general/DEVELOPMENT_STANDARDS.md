# BlackwallV2 Development Standards

## Directory Structure Guidelines

This document outlines the standardized development practices for the BlackwallV2 project to maintain clean, efficient code organization.

### Directory Structure

```text
Implementation/
├── benchmarks/    # Performance testing scripts
├── copilot/       # AI assistance integration and journals
├── demo/          # Demonstration scripts
├── docs/          # Documentation organized by topic
│   ├── general/   # General project documentation
│   ├── media/     # Media integration documentation
│   ├── systems/   # System-specific documentation
│   └── optimization/ # Optimization documentation
├── integration/   # System integration components
├── llm_integration/ # LLM integration module
├── log/           # System logs (auto-generated)
├── media/         # Media handling module
├── memlong/       # Long-term memory module
├── memshort/      # Short-term memory module
├── monitoring/    # System monitoring tools
├── optimize/      # Optimization algorithms and tools
├── profile_results/ # Profiling output (auto-generated)
├── root/          # Core system components
├── samples/       # Example files and test data
├── scripts/       # Utility and operation scripts
│   └── batch/     # Batch scripts for system operations
├── test/          # Test scripts and modules
├── test_files/    # Test data files
└── tools/         # Utility tools and scripts
```

## File Placement Guidelines

1. **Code Files**:
   - **Core modules** belong in `root/`
   - **Demo scripts** belong in `demo/`
   - **Test scripts** belong in `test/`
   - **Utility scripts** belong in `tools/` or `scripts/`

2. **Documentation**:
   - All documentation files (`.md`) should be placed in the `docs/` directory
   - Topic-specific documentation should go in appropriate subdirectories

3. **Batch Files**:
   - All `.bat` files should be placed in `scripts/batch/`
   - Name batch files clearly to indicate their function

4. **Logs and Output**:
   - Log files should be written to the `log/` directory
   - Profile results should be written to `profile_results/`
   - Never write logs or results to the root directory

## Code Standards

1. **Logging**:
   - Always use the standardized logging module (`demo_logging.py`) for demos
   - Log files should have timestamps in filenames
   - Always log to the proper directory (`log/`)

2. **Imports**:
   - Use relative imports when importing from project modules
   - Avoid hardcoded paths; use directory discovery instead

3. **File Naming**:
   - Use snake_case for Python files
   - Use descriptive names that indicate functionality

4. **Documentation**:
   - Document all new modules with docstrings
   - Update relevant documentation when adding new features

## Version Control Practices

1. **Commits**:
   - Make small, focused commits
   - Write clear commit messages that explain the change

2. **Branches**:
   - Create feature branches for new development
   - Use hotfix branches for urgent fixes

3. **Pull Requests**:
   - Submit pull requests for review before merging to main
   - Ensure all tests pass before merging

4. **Regular Housekeeping**:
   - Conduct regular code reviews to maintain standards
   - Periodically review for organization issues
   - Clean up unused code and remove duplicates

## Before Contributing

1. Verify your changes adhere to the directory structure
2. Run tests to ensure functionality is preserved
3. Ensure your code follows the project's coding standards
4. Document any API changes or new features

By following these standards, we can prevent disorganization and maintain a clean, efficient codebase.
