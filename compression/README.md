# UML Compression Engine Prototype

A prototype implementation of the Universal Mathematical Language Compression Engine (UML:CE) with support for both lossless and lossy compression modes.

## Features

- **Dual Mode Compression**: Lossless and lossy compression modes
- **Batch Processing**: Heartbeat-style processing in configurable batches
- **Base-52 Encoding**: Custom UML encoding for text compression
- **File Type Detection**: Automatic detection and appropriate algorithm selection
- **Error Handling**: Built-in verification and error reporting
- **AI Integration**: Callback support and structured JSON output
- **CLI Interface**: Command-line tool for manual and automated use

## Quick Start

### 1. Create Test Files

First, create some sample files for testing:

```bash
python test_compression.py create-samples
```

This creates a `test_files/` directory with sample text and Python files.

### 2. Add Your Own Test Files

Add your test files to the `test_files/` directory:
- **Text files**: `.txt`, `.py`, `.md`
- **Image files**: `.jpg`, `.png`
- **Audio files**: `.mp3`, `.wav`
- **Video files**: `.mp4`, `.avi`

### 3. Run Tests

Test compression on all files:

```bash
python test_compression.py
```

### 4. Manual Compression

Use the CLI for individual files:

```bash
# Lossless compression
python uml_compression_engine.py compress input.txt output.cmp --mode lossless

# Lossy compression (for text files)
python uml_compression_engine.py compress input.txt output.cmp --mode lossy

# Custom batch size
python uml_compression_engine.py compress input.txt output.cmp --batch-size 2048
```

## Current Implementation Status

### ✅ Implemented
- Core compression engine framework
- Lossless compression using zlib and base-52 encoding
- Lossy text compression using simple summarization
- Batch/heartbeat processing
- File type detection
- Basic verification
- CLI interface
- Progress callbacks
- JSON metadata storage

### 🚧 In Progress
- Round-trip verification (decompress and compare)
- Magic square-based compression for images/audio
- Advanced lossy algorithms
- Full decompression implementation

### 📋 Planned
- Channel-separated image compression
- Nested/layered compression
- AI-driven parameter optimization
- Web UI with drag-and-drop
- Plugin system for custom algorithms
- Encryption module

## File Structure

```
compression/
├── uml_compression_engine.py  # Main compression engine
├── test_compression.py        # Test script
├── README.md                  # This file
├── test_files/               # Test files directory
└── test_files/compressed/    # Compressed output directory
```

## Algorithm Details

### Lossless Mode
- **Text files**: Base-52 dictionary encoding with frequency analysis
- **Binary files**: Standard zlib compression
- **Verification**: Hash comparison and size checks

### Lossy Mode
- **Text files**: Simple summarization (first sentence per paragraph) + base-52 encoding
- **Other files**: Falls back to lossless (temporary)

### Base-52 Encoding
- Uses frequency analysis to build dictionaries of common words
- Maps top 52 frequent words to single characters (A-Z, a-z)
- Stores dictionary alongside compressed data for decompression

## Testing Your Files

The test script will automatically:
1. Find all supported files in `test_files/`
2. Test both lossless and lossy compression (where applicable)
3. Show compression ratios and performance metrics
4. Verify compressed files can be processed
5. Generate a summary report

## Next Steps

1. **Add your test files** to `test_files/`
2. **Run the tests** to see current performance
3. **Review results** and identify areas for improvement
4. **Implement missing features** based on test outcomes

## AI Integration

The engine supports AI integration through:
- Progress callbacks for real-time monitoring
- Structured JSON output for easy parsing
- Configurable parameters for optimization
- Error reporting and logging

Example AI usage:
```python
from uml_compression_engine import UMLCompressionEngine

engine = UMLCompressionEngine()

def ai_callback(info):
    # AI can monitor progress and adjust parameters
    print(f"AI received: {info}")

result = engine.compress(
    "data.txt", "data.cmp", 
    mode="lossless",
    callback=ai_callback
)

# AI can parse structured result
if result['status'] == 'success':
    ratio = result['compression_ratio']
    # AI decision logic here
```
