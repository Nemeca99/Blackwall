#!/usr/bin/env python3
"""
Test script for UML Compression Engine
"""

import hashlib
import sys
from pathlib import Path
from uml_compression_engine import UMLCompressionEngine

def test_compression(test_files_dir: str = "test_files"):
    """Test compression on various file types."""
    
    engine = UMLCompressionEngine()
    
    # Create test directory if it doesn't exist
    test_dir = Path(test_files_dir)
    test_dir.mkdir(exist_ok=True)
    
    # Create output directory
    output_dir = test_dir / "compressed"
    output_dir.mkdir(exist_ok=True)
    
    print("=== UML Compression Engine Test ===\n")
    
    # Find test files
    test_files = []
    for ext in ['.txt', '.py', '.md', '.jpg', '.png', '.mp3', '.wav', '.mp4', '.avi']:
        files = list(test_dir.glob(f"*{ext}"))
        test_files.extend(files)
    
    if not test_files:
        print(f"No test files found in {test_files_dir}/")
        print("Please add some test files:")
        print("- .txt, .py, .md (text files)")
        print("- .jpg, .png (image files)")  
        print("- .mp3, .wav (audio files)")
        print("- .mp4, .avi (video files)")
        return
    
    print(f"Found {len(test_files)} test files:")
    for f in test_files:
        print(f"  - {f.name}")
    print()
    
    # Test each file with different modes
    results = []
    
    for test_file in test_files:
        print(f"Testing: {test_file.name}")
        print("-" * 40)
        
        # Test lossless compression
        output_lossless = output_dir / f"{test_file.stem}_lossless.cmp"
        
        def progress_callback(info):
            if 'progress' in info:
                stage = info['stage'].replace('_', ' ').title()
                print(f"  {stage}: {info['progress']*100:.1f}%")
        
        print("  Mode: Lossless")
        result_lossless = engine.compress(
            str(test_file),
            str(output_lossless),
            mode='lossless',
            callback=progress_callback
        )
        
        results.append(result_lossless)
        
        if result_lossless['status'] == 'success':
            ratio = result_lossless['compression_ratio']
            savings = (1 - ratio) * 100
            print(f"  ✓ Success! Compression ratio: {ratio:.3f} ({savings:.1f}% savings)")
            print(f"    Original: {result_lossless['original_size']:,} bytes")
            print(f"    Compressed: {result_lossless['compressed_size']:,} bytes")
            print(f"    Time: {result_lossless['processing_time']:.2f}s")
        else:
            print(f"  ✗ Failed: {result_lossless.get('error', 'Unknown error')}")
        
        # Test lossy compression (for text files)
        file_type = engine.detect_file_type(str(test_file))
        if file_type == 'text':
            print("\n  Mode: Lossy")
            output_lossy = output_dir / f"{test_file.stem}_lossy.cmp"
            
            result_lossy = engine.compress(
                str(test_file),
                str(output_lossy),
                mode='lossy',
                callback=progress_callback
            )
            
            results.append(result_lossy)
            
            if result_lossy['status'] == 'success':
                ratio = result_lossy['compression_ratio']
                savings = (1 - ratio) * 100
                print(f"  ✓ Success! Compression ratio: {ratio:.3f} ({savings:.1f}% savings)")
                print(f"    Original: {result_lossy['original_size']:,} bytes")
                print(f"    Compressed: {result_lossy['compressed_size']:,} bytes")
                print(f"    Time: {result_lossy['processing_time']:.2f}s")
        
        # Test decompression
        print("\n  Mode: Decompression (Round-Trip Test)")
        
        # For lossless mode we can compare with the original
        output_decompressed = output_dir / f"{test_file.stem}_decompressed{test_file.suffix}"
        
        result_decompress = engine.decompress(
            str(output_lossless),
            str(output_decompressed),
            callback=progress_callback
        )
        
        results.append(result_decompress)
        
        if result_decompress['status'] == 'success':
            print("  ✓ Success! File decompressed")
            print(f"    Compressed: {result_decompress['compressed_size']:,} bytes")
            print(f"    Decompressed: {result_decompress['decompressed_size']:,} bytes")
            print(f"    Time: {result_decompress['processing_time']:.2f}s")
            
            # Check if the decompressed file matches the original for lossless modes
            def calculate_file_hash(filepath):
                with open(filepath, 'rb') as file:
                    return hashlib.sha256(file.read()).hexdigest()
            
            orig_hash = calculate_file_hash(str(test_file))
            decomp_hash = calculate_file_hash(str(output_decompressed))
            
            if orig_hash == decomp_hash:
                print("  ✓ Verification: Perfect round-trip (hashes match)")
            else:
                print("  ⚠ Verification: Round-trip produced different file (hashes don't match)")
                print(f"    Original hash: {orig_hash[:8]}...")
                print(f"    Decompressed hash: {decomp_hash[:8]}...")
        else:
            print(f"  ✗ Failed: {result_decompress.get('error', 'Unknown error')}")
        
        print("\n")
    
    # Summary
    print("=== Test Summary ===")
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] != 'success']
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if successful:
        # Filter only compression results, not decompression for average calculation
        compression_results = [r for r in successful if 'compression_ratio' in r]
        if compression_results:
            avg_ratio = sum(r['compression_ratio'] for r in compression_results) / len(compression_results)
            avg_savings = (1 - avg_ratio) * 100
            print(f"Average compression ratio: {avg_ratio:.3f} ({avg_savings:.1f}% savings)")
            
            # Only consider compression results for total calculations
            total_original = sum(r.get('original_size', 0) for r in compression_results)
            total_compressed = sum(r.get('compressed_size', 0) for r in compression_results)
            total_savings = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
            print(f"Total space saved: {total_original - total_compressed:,} bytes ({total_savings:.1f}%)")
    
    if failed:
        print("\nFailed tests:")
        for r in failed:
            print(f"  - {r['input']}: {r.get('error', 'Unknown error')}")

def create_sample_files(test_files_dir: str = "test_files"):
    """Create some sample files for testing if none exist."""
    
    test_dir = Path(test_files_dir)
    test_dir.mkdir(exist_ok=True)
    
    # Sample text file
    sample_text = """# Sample Text File

This is a sample text file for testing compression.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

This text contains repeated words and patterns that should compress well with dictionary-based compression. The compression engine should be able to identify common words and patterns.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. This sentence is repeated to test compression efficiency.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. This sentence is repeated to test compression efficiency.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. This sentence is repeated to test compression efficiency.
"""
    
    with open(test_dir / "sample.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    # Sample Python file
    sample_py = '''#!/usr/bin/env python3
"""Sample Python file for testing compression."""

def hello_world():
    """Print hello world message."""
    print("Hello, World!")
    return "Hello, World!"

def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    """Main function."""
    hello_world()
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
'''
    
    with open(test_dir / "sample.py", "w", encoding="utf-8") as f:
        f.write(sample_py)
    
    print(f"Created sample files in {test_files_dir}/")
    print("You can add your own test files (images, audio, video) to this directory.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create-samples":
        create_sample_files()
    else:
        test_compression()
