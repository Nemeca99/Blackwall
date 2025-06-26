# Compression System Design Document

This document outlines the design for a custom compression system supporting both lossless and lossy modes. The goal is to provide a unified tool for compressing data in the UML Calculator ecosystem, with lossless compression for critical data (e.g., LTM, code, documents) and lossy compression for less critical data (e.g., images, audio, logs).

---

## Requirements

### Functional Requirements
- Support both lossless and lossy compression modes
- Allow user to select mode per file or data type
- Provide CLI and/or API for integration
- Support common file types: text, binary, images, audio
- Auto-detect file type and suggest best mode (optional)
- Modular design for easy extension with new algorithms

### Non-Functional Requirements
- Fast compression/decompression for typical file sizes
- Reasonable memory usage
- Cross-platform compatibility (Windows, Linux, Mac)
- Open, documented format for archives
- Support for AI/automation workflows (API, CLI, and programmatic integration)
- Robust error handling, logging, and automated verification of compression/decompression
- Designed for future support of encryption and advanced security features

---

## Use Cases
- Compressing LTM data for archival (lossless)
- Compressing logs or telemetry for storage (lossy)
- Archiving project files (lossless)
- Reducing size of images/audio for sharing (lossy)
- Automated, AI-driven batch compression and decompression for large datasets
- Integration with RIS, UML, Lyra, and TREES systems for seamless data exchange and storage
- Use by technical users (developers, researchers) via API/CLI for pipelines and automation
- Use by non-technical users through a simple drag-and-drop UI for everyday file compression
- Real-time or scheduled compression jobs managed by AI agents
- Compression of logs, telemetry, and LTM data as part of automated workflows
- On-the-fly compression for data ingestion or export in larger ecosystem applications

---

## Architecture

### High-Level Structure
- **Compressor Core**: Unified interface for compression/decompression
- **Lossless Module**: Implements or wraps lossless algorithms (e.g., zlib, LZMA, custom)
- **Lossy Module**: Implements or wraps lossy algorithms (e.g., JPEG, MP3, custom quantization)
- **File Type Detector**: Suggests best mode/algorithm based on file type
- **CLI/API Layer**: User interface for compression tasks

### Data Flow
1. User selects file(s) and mode (or uses auto-detect)
2. File Type Detector analyzes input (optional)
3. Compressor Core routes to Lossless or Lossy module
4. Data is compressed and output to archive or file
5. Decompression reverses the process

---

### Modular Architecture Overview
- **Compressor Core:** Unified interface for compression/decompression logic
- **Plugin System:** Pluggable modules for algorithms, file type handlers, and experimental features
- **User Interface (UI):** Drag-and-drop GUI and CLI for user interaction
- **API Layer:** Python API and/or REST endpoints for programmatic and AI access
- **AI Integration Hooks:** Callbacks, structured output, and automation support
- **Extension Points:** Easy addition of new algorithms, file types, and AI modules via registration or plugin interface
- **Metadata & Logging:** Centralized logging, error reporting, and metadata management for all operations

This modular design ensures flexibility, extensibility, and seamless integration with other systems and AI workflows.

---

## Algorithm Options

### Lossless
- zlib/DEFLATE (fast, widely supported)
- LZMA (high compression, slower)
- Custom (e.g., RLE, Huffman, LZ77/78)

### Lossy
- JPEG (images)
- MP3/OGG (audio)
- Custom quantization (for text/logs or specialized data)

---

## Extensibility
- New algorithms can be added as plugins/modules
- Support for new file types via handler registration
- Configurable compression levels and parameters
- All algorithms are implemented as pluggable modules, allowing easy addition or replacement
- Support for hybrid/multi-stage compression (e.g., dictionary + base-52, or magic square + standard)
- Extension points for new algorithms and file type handlers via plugin registration
- Modular design enables experimentation with custom, experimental, or AI-driven algorithms

---

## User Interface

### CLI Example
```
compressor.py compress myfile.txt --mode lossless
compressor.py compress photo.jpg --mode lossy --quality 70
compressor.py decompress archive.cmp
```

### API Example
```python
compress('myfile.txt', 'myfile.cmp', mode='lossless')
compress('photo.jpg', 'photo.cmp', mode='lossy', quality=70)
```

---

## User Interface (UI) Design: Simplicity and Workflow

### Design Goals
- **Simplicity:** Minimal steps, clear choices, and intuitive layout.
- **Drag-and-Drop:** Users can drag files/folders into the UI to begin.
- **Guided Workflow:** Step-by-step process with only relevant options shown at each stage.
- **Accessibility:** UI is designed for keyboard navigation, screen readers, and users with disabilities.
- **Localization:** Support for multiple languages and regional formats.
- **Expert/Advanced Mode:** Optional mode exposing all settings, batch scripting, and direct AI integration for power users.

### Example Workflow
1. **Drag and Drop:** User drags files or folders into the application window.
2. **Select Compression Mode:**
   - Choose between Lossless or Lossy.
3. **Select Data Type:**
   - Text, Image, Audio, Video, or Auto-detect.
4. **Set Compression Preferences:**
   - For Lossless: Choose speed vs. ratio, batch size, encoding scheme, etc.
   - For Lossy: Set compression level (slider), accuracy, summarization, or quality.
5. **Review and Confirm:**
   - Show summary of settings and estimated output size/quality.
6. **Compress:**
   - Start compression and show progress bar.
7. **Download/Save:**
   - User downloads or saves the compressed archive and any metadata files.

### Step-by-Step Workflow (User Perspective)
1. **Drag-and-drop** file(s) onto the interface.
2. **Select compression format:** Lossless or Lossy.
3. **Click "Next"** to proceed.
4. **Choose data type:** Text, Image, Audio, etc.
5. **Select compression level:** (e.g., "Maximum Compression" vs. "Maximum Accuracy").
6. **Adjust advanced options** if needed (batch size, encoding, channel separation, etc.).
7. **Confirm and run compression.**

### UI Elements
- **Main Window:** Drag-and-drop area, file list, and action buttons.
- **Mode Selector:** Toggle or radio buttons for Lossless/Lossy.
- **Type Selector:** Dropdown or auto-detect for file type.
- **Compression Settings:** Sliders, dropdowns, or advanced options panel.
- **Progress Bar:** Shows compression progress and estimated time.
- **Summary Panel:** Displays chosen options and estimated results.

### Accessibility and Help
- Tooltips and help icons for each option.
- Sensible defaults for non-expert users.
- Advanced options hidden unless requested.

---

## User Options and Configurability

A key part of UML:CE is giving users control over how their data is compressed. The system should provide flexible options for:

- **Compression Mode:**
  - Lossless (exact recovery)
  - Lossy (summarization, quantization, or other reduction)
  - Hybrid (user can select per file or batch)
- **Batch/Heartbeat Size:**
  - User can set the size of batches for processing (e.g., paragraph, block, or custom size)
- **Dictionary Depth:**
  - Number of layers of dictionary compression (single or nested)
  - Option to tune dictionary size or frequency threshold
- **Encoding Scheme:**
  - Choose between standard encoding, base-52 UML, or custom symbol sets
- **Channel/Component Separation:**
  - For images/audio, option to separate and compress channels independently
- **Metadata Inclusion:**
  - Option to include or exclude metadata (timestamps, permissions, etc.)
- **Compression Level:**
  - Trade-off between speed and compression ratio (e.g., fast, balanced, maximum)
- **Advanced/Experimental Features:**
  - Enable/disable nested compression, magic square encoding, or other experimental modules
- **Save/Load Presets:** Users and AI agents can save and load compression settings as named presets for repeatable workflows.
- **Headless Mode:** Full support for running all operations via API or CLI without any UI, enabling automation and integration in scripts or pipelines.

### Example CLI/API Options
```
compressor.py compress myfile.txt --mode lossless --batch-size 1024 --dict-depth 2 --encoding base52 --compression-level max
compressor.py compress image.png --mode lossy --channels separate --magic-square on
```

### Integration Guidance
- All options should be available via both CLI and API.
- Provide sensible defaults for non-expert users, but allow full control for advanced users.
- Document each option clearly in help messages and documentation.

---

## Open Questions / To Refine

- **What file types are highest priority?**
  - Priority will depend on the final format chosen for LTM (Long-Term Memory). Next priority is any text-related files (logs, configs, plain text, etc.).
- **Should we support multi-file archives (like ZIP)?**
  - (To be decided; could be useful for batch operations or LTM snapshots.)
- **What metadata should be stored (timestamps, permissions, etc.)?**
  - Yes, include metadata (timestamps, permissions, etc.)—it won’t hurt and may be useful for future features.
- **Should lossy mode support custom quantization for text/logs?**
  - Yes, lossy mode will be needed for text/logs and should support custom quantization or reduction strategies.
- **How should we handle encryption or password protection?**
  - Encryption will be added later, using a custom scheme based on magic squares.
- **What is the minimum viable product (MVP) for first release?**
  - MVP is achieved when the compressor works with Lyra (integration milestone), even if only for a subset of file types.

---

## Open Questions, Future Ideas & To-Do

- **Encryption:** Design and integrate a magic square-based encryption module for secure compression (future phase).
- **Distributed/Cloud Compression:** Support for distributed or cloud-based batch compression jobs.
- **Self-Optimizing AI:** Use AI to tune compression parameters dynamically based on data type, history, or user feedback.
- **Cross-Platform Packaging:** Streamlined packaging and deployment for all major OSes.
- **Mobile Support:** Explore lightweight/mobile-friendly versions of the compressor.
- **Visualization Tools:** Add tools for visualizing compression results, errors, and performance metrics.
- **User Feedback Loop:** Mechanism for users/AI to submit feedback or improvement suggestions directly from the UI/API.
- **Integration with Other Ecosystem Tools:** Deeper hooks for RIS, UML, Lyra, TREES, and future systems.
- **Test Suite & Validation:** Comprehensive automated tests for all features, edge cases, and performance.
- **Documentation:** Expand user and developer documentation, including API references and integration guides.
- **Internationalization:** Broader language and locale support.
- **Accessibility Audits:** Regular accessibility reviews and improvements.

---

## UML:CE (Universal Mathematical Language Compression Engine) - Conceptual Design

### Heartbeat-Inspired Compression Workflow

- **Batch Processing:** The engine processes data in logical batches or "heartbeats," summarizing and compressing each chunk in turn. The batch size and rate can adapt based on data type, size, or system load.

### 1. Lossless Mode
- **Approach:** Convert data to base-52 UML encoding for compact, reversible representation.
- **Text:** Directly encode as base-52 symbols.
- **Binary:** Encode as base-52 symbols or use a reversible mapping.
- **Benefit:** Simple, effective for text and structured data.

### 2. Lossy Mode (Summary Batch Lossy)
- **Text:**
  - Split input into logical groups (e.g., paragraphs).
  - Summarize each group (e.g., paragraph → sentence or key points).
  - Encode the summary in base-52 UML.
  - Result: Highly compressed, meaning-preserving, but not bit-exact.
- **Image/Video:**
  - Treat each pixel or block as a “magic square” (apply a mathematical transformation or encoding).
  - Summarize regions (e.g., average color, edge detection, or feature extraction).
  - Encode region summaries in base-52 or another compact form.
- **Audio/Music:**
  - Summarize waveform segments (e.g., extract dominant frequencies, envelope, or features).
  - Encode features or summaries in base-52 or as “magic square” values.

### 3. Magic Square Encoding
- For images/audio, each pixel or sample can be transformed using a magic square-based algorithm, adding mathematical structure and potential for further compression or encryption.

### 4. Adaptive Heartbeat
- The “heartbeat” (batch size/rate) can be tuned dynamically, allowing the engine to adapt to different data types and system conditions.

---

## Next Steps for UML:CE
1. Document detailed algorithms for each mode and data type.
2. Prototype text summarization + base-52 encoding.
3. Define and prototype magic square encoding for images/audio.
4. Implement batch/heartbeat processing logic.
5. Integrate with Lyra and test on representative data.

---

## Magic Square-Based Pixel Compression (Concept)

This approach uses mathematical magic squares as the basis for pixel (or block) compression, enabling scalable fidelity and adaptive compression for images.

### Key Concepts
- **Base Unit:** Each pixel or image block is represented by a magic square (e.g., 3x3 for standard, 6x6 or 10x10 for higher fidelity).
- **Value Range:** Each cell in the magic square holds a value from 0–255 (like standard 8-bit color channels).
- **Hierarchical Control:**
  - The top 3x3 square of each block acts as a control layer, determining the brightness/contrast for the block below it.
  - This control layer influences how the underlying data is interpreted or displayed.
- **Color Channels:**
  - Each color channel (R, G, B) is treated as a separate frame/layer.
  - Overlaying the three magic square matrices reconstructs the full-color image.
- **Hierarchical Influence:**
  - Each control square (top 3x3) can affect multiple underlying squares, allowing for scalable fidelity and adaptive compression.
  - Larger blocks (6x6, 10x10) provide more detail, while smaller ones compress more aggressively.

### Example Workflow
1. **Divide** the image into blocks (e.g., 6x6 or 10x10).
2. **Extract** the top 3x3 region of each block as the control layer.
3. **Encode** the control layer and the underlying data separately.
4. **Overlay** R, G, B channel matrices to reconstruct the image.
5. **Adjust** block size for desired fidelity/compression ratio.

### Notes
- This method is experimental and may require tuning for visual quality and compression efficiency.
- The mathematical structure of magic squares may offer unique properties for error correction or encryption.
- Further research and prototyping are needed to evaluate real-world performance.

---

## Experimental: Nested and Channel-Separated Compression for Images

### Concept
- **Channel Separation:**
  - During compression, split the image into three separate files: one for Red, one for Green, and one for Blue channel values.
  - Each channel is compressed independently, potentially using different parameters or algorithms for each.
- **Rebuild File:**
  - A fourth file is created to store metadata or instructions for reconstructing the original image from the three channels (e.g., alignment, offsets, any special transforms).
  - This rebuild file is also compressed.
- **Final Nesting:**
  - All four files (R, G, B, and rebuild) are then bundled and compressed together as a final archive or package.

### Potential Benefits
- May exploit redundancy or patterns unique to each color channel, improving compression for certain images.
- Allows for channel-specific optimizations (e.g., more aggressive compression for less perceptually important channels).
- The rebuild file can enable advanced features (e.g., error correction, partial recovery, or progressive loading).

### Workflow Example
1. **Split** image into R, G, B channel data.
2. **Compress** each channel separately (using your magic square or base-52 method, or other custom logic).
3. **Create** a rebuild file with metadata for reassembly.
4. **Compress** the rebuild file.
5. **Bundle** all four files and apply a final compression pass (nested compression).

### Notes
- This is an experimental approach and may require tuning for efficiency and quality.
- Could be extended to other multi-channel data (e.g., audio with multiple tracks, video with YUV channels).
- Further research and prototyping are needed to evaluate real-world performance and practicality.

---

## Experimental: Layered Compression Dictionaries for Text

### Concept
- **Per-Layer Dictionaries:**
  - Each time text is compressed, a unique dictionary is generated for that specific layer of compression.
  - If nested (multi-layer) compression is used, each layer has its own dictionary file, tailored to the patterns found at that stage.
- **Workflow:**
  1. Analyze the text batch and build a dictionary of most frequent words, phrases, or patterns.
  2. Replace those patterns with compact codes (symbols, numbers, or base-52 tokens).
  3. Store the dictionary alongside the compressed data for that layer.
  4. If further compression is applied, repeat the process: build a new dictionary for the next layer, compress, and store.
- **Decompression:**
  - Decompression reverses the process, using the dictionaries in reverse order (last layer first, up to the original text).

### Potential Benefits
- Adapts to the specific redundancy and vocabulary of each batch/layer, potentially improving compression ratio.
- Allows for highly customized, context-aware compression.
- Each layer can use different strategies or optimizations.

### Notes
- This approach increases metadata (dictionary files), but may be offset by better compression.
- Could be combined with summarization or other lossy steps for hybrid compression.
- Further research and prototyping are needed to evaluate efficiency and practicality.

---

## Practical Implementation Guidance: UML:CE Prototyping Steps

### 1. Lossless Text Compression with Per-Batch Dictionary and Base-52 Encoding

#### Overview
- Split text into batches (e.g., paragraphs or fixed-size blocks).
- For each batch, build a dictionary of the most frequent words/phrases.
- Replace those patterns with compact codes (e.g., numbers, base-52 tokens).
- Store the dictionary alongside the compressed batch.
- Optionally, apply base-52 encoding to the compressed output for further compaction and UML integration.

#### Example Python Pseudocode
```python
import re
from collections import Counter

BASE52_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def to_base52(n):
    if n == 0:
        return BASE52_ALPHABET[0]
    chars = []
    while n > 0:
        chars.append(BASE52_ALPHABET[n % 52])
        n //= 52
    return ''.join(reversed(chars))

def compress_batch(text):
    words = re.findall(r'\w+', text)
    freq = Counter(words)
    # Build dictionary: top N frequent words
    dictionary = {word: idx for idx, (word, _) in enumerate(freq.most_common(52))}
    # Replace words with codes
    tokens = [to_base52(dictionary[w]) if w in dictionary else w for w in words]
    return tokens, dictionary
```

### 2. Batch/Heartbeat Compressor Framework

#### Overview
- Process data in logical batches ("heartbeats").
- For each batch, apply compression (lossless or lossy) and store results.
- Can be extended to images/audio by swapping in the appropriate batch compressor.

#### Example Python Pseudocode
```python
def heartbeat_compress(data, batch_size, compress_fn):
    batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
    compressed_batches = []
    for batch in batches:
        compressed, dictionary = compress_fn(batch)
        compressed_batches.append((compressed, dictionary))
    return compressed_batches
```

### 3. Extending with UML and Magic Square Concepts
- After dictionary compression, encode the output using your base-52 UML scheme for symbolic compactness.
- For images/audio, use the magic square-based block encoding as described in earlier sections.
- For nested/layered compression, repeat the process: compress the output of one layer with a new dictionary and encoding.

### 4. Decompression Guidance
- Decompression reverses the process: decode base-52, use the dictionary to reconstruct the original batch, and repeat for each layer if nested.

### 5. Integration Notes
- The framework is modular: you can swap in new compressors, summarizers, or encoders for each data type or batch.
- Store metadata (dictionaries, batch sizes, encoding info) alongside compressed data for full reversibility.

---

## Summary
This section provides a practical, step-by-step guide for implementing the core ideas of UML:CE, blending standard and custom approaches. You can use these as a foundation for prototyping, testing, and further innovation.

---

## Next Steps
1. Review and refine requirements and architecture
2. Select initial algorithms for each mode
3. Prototype CLI and API
4. Test with representative data
5. Iterate based on feedback

---

### AI Integration Hooks

To support AI agents, automation, and programmatic workflows, UML:CE will provide:
- **API Endpoints / Callable Functions:** Expose all major features (compression, decompression, option selection) via a Python API and/or REST endpoints.
- **Scriptable CLI:** All CLI options are machine-friendly and can be invoked by scripts or AI agents.
- **Structured Output:** Compression and decompression results, including metadata, are available in machine-readable formats (e.g., JSON, YAML) for easy parsing by AI.
- **Batch Processing:** Support for batch jobs and automated workflows, allowing AI to process multiple files or datasets in sequence.
- **Hooks/Callbacks:** Optional hooks for AI to receive progress updates, intermediate results, or to adjust options dynamically during processing.

**Example Python API Call:**
```python
result = compress_file(
    input_path='data.txt',
    output_path='data.cmp',
    mode='lossless',
    batch_size=1024,
    callback=my_progress_hook
)
# result: {'status': 'success', 'output': 'data.cmp', 'ratio': 0.42, 'log': '...'}
```

**Example JSON Response:**
```json
{
  "status": "success",
  "input": "data.txt",
  "output": "data.cmp",
  "mode": "lossless",
  "compression_ratio": 0.42,
  "log": "Compression completed successfully.",
  "metadata": {"batch_size": 1024, "algorithm": "base52"}
}
```

- **Webhook/Callback Support:** AI agents and automation can register webhooks or callback functions to receive real-time progress updates, error notifications, and completion events.

---

## Error Handling & Verification (Expanded)

- **Automated Round-Trip Verification:** After compressing each file or batch, immediately decompress and compare to the original (for lossless mode).
- **Configurable Verification Depth:** Allow users/AI to choose full byte-for-byte comparison, sample-based checks (for very large files), or hash-based verification for speed.
- **Error Severity Levels:** Classify errors as warnings (minor mismatch), recoverable (can retry with fallback), or critical (halt process and alert).
- **Smart Retry Logic:** On failure, automatically retry compression with safer/fallback settings or alternative algorithms.
- **AI-Assisted Anomaly Detection:** Use AI to flag repeated failures, unusual patterns, or data that consistently resists compression.
- **User/AI Notification Hooks:** Provide real-time alerts, structured error reports, and logs accessible to both users and AI agents.
- **Paranoid Mode:** Optional ultra-strict mode for critical data—multiple verification passes, cross-algorithm checks, and redundant storage.
- **Performance & Resource Logging:** Log compression time, ratio, memory/CPU usage, and verification results for optimization and AI feedback.
- **Failed Case Archiving:** Optionally save failed or problematic files/batches for later analysis, debugging, or AI learning.
- **Lossy Mode Metrics:** For lossy compression, log similarity scores, quality metrics, and flag extreme deviations for review.

These strategies ensure robust, transparent, and AI-friendly error handling, supporting both manual and automated workflows.

---

## Solo Developer Notes & Strategy

- **Prioritize Core Features:** Focus on MVP and essential workflows before tackling experimental or advanced features.
- **Track Open Questions:** Maintain a running list of unresolved issues, ideas, and “someday” features (see Open Questions section).
- **Automate Repetitive Tasks:** Use scripts, templates, and AI tools to reduce manual work and speed up development.
- **Iterate in Small Steps:** Build, test, and document in small, manageable increments—each working piece is progress.
- **Document as You Go:** Keep design docs, code comments, and user guides up to date to avoid knowledge loss.
- **Celebrate Progress:** Acknowledge milestones, even small ones, to stay motivated.
- **Ask for Help When Needed:** Don’t hesitate to leverage open source, forums, or AI assistants for tricky problems.
- **Balance Ambition and Realism:** It’s okay to defer or drop features that don’t fit the current scope or resources.
- **Self-Care:** Take breaks, avoid burnout, and remember that progress—even slow—is still progress.

This section is for your personal workflow, reminders, and strategy as you build and evolve the project.

---
