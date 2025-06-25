# Developer Notes & Troubleshooting

This file contains developer notes, troubleshooting tips, and documentation pointers for the Lyra Blackwall system.

## Documentation

- SYSTEMS_SUMMARY.md: Main system blueprint
- Build_Change_Log.md: Build and migration history
- DEVELOPER_GUIDE.md: Comprehensive development guidelines
- IMPLEMENTATION_STATUS.md: Current implementation status

## Troubleshooting

- For import errors, check directory structure and use relative imports with `.` prefix
- For memory access errors, verify the existence of memshort/stm_buffer.json and memlong/ltm_buffer.json
- Log files are stored in the /log/ directory with BLACKWALL_LOGS.md as the main log file
- If LLM integration fails, check config.json in the llm_integration directory

## Module Interaction

- All modules should interact through the Body class (central event bus)
- Hemisphere modules (Left_Hemisphere and Right_Hemisphere) are accessed via the Brainstem
- External modules (including LLM integration) should not directly access internal modules

## Testing

- Run run_integration_test.bat to verify basic module imports
- Run run_blackwall_demo.bat to test the core system functionality
- Run run_llm_demo.bat to test the LLM integration

## Additional Resources

- ../README.md: Main project documentation
- ../personality/README.md: Fragment system documentation
- ../llm_integration/README.md: LLM integration documentation
- Run test scripts in the demo/ directory for functionality examples
