#!/usr/bin/env python3
"""
Compare original and decompressed files to identify differences
"""

import sys
import os
import difflib
from pathlib import Path

def compare_files(original_file, decompressed_file):
    """Compare original and decompressed files to identify differences."""
    
    print(f"Comparing files:")
    print(f"  Original: {original_file}")
    print(f"  Decompressed: {decompressed_file}")
    print("-" * 80)
    
    with open(original_file, 'r', encoding='utf-8') as f1:
        original_lines = f1.readlines()
        
    with open(decompressed_file, 'r', encoding='utf-8') as f2:
        decompressed_lines = f2.readlines()
    
    # Get file stats
    original_chars = sum(len(line) for line in original_lines)
    decompressed_chars = sum(len(line) for line in decompressed_lines)
    
    print(f"Original: {len(original_lines)} lines, {original_chars} characters")
    print(f"Decompressed: {len(decompressed_lines)} lines, {decompressed_chars} characters")
    print()
    
    # Calculate differences
    diff = list(difflib.unified_diff(
        original_lines, 
        decompressed_lines,
        fromfile='original',
        tofile='decompressed',
        lineterm=''
    ))
    
    if diff:
        print("Differences found:")
        for line in diff[:50]:  # Limit to first 50 diff lines
            print(line)
        
        if len(diff) > 50:
            print(f"... and {len(diff) - 50} more differences")
    else:
        print("Files are identical.")
    
    # Analyze character-level differences
    print("\nCharacter-level analysis:")
    
    # Check if files have similar structure but different whitespace
    stripped_original = [line.strip() for line in original_lines]
    stripped_decompressed = [line.strip() for line in decompressed_lines]
    
    if stripped_original == stripped_decompressed:
        print("✓ Files differ only in whitespace/indentation")
    
    # Check first few characters where they start to differ
    min_len = min(original_chars, decompressed_chars)
    original_text = ''.join(original_lines)
    decompressed_text = ''.join(decompressed_lines)
    
    for i in range(min_len):
        if original_text[i] != decompressed_text[i]:
            print(f"First difference at position {i}:")
            context_start = max(0, i - 20)
            context_end = min(min_len, i + 20)
            
            original_context = original_text[context_start:context_end]
            decompressed_context = decompressed_text[context_start:context_end]
            
            # Mark the differing character
            if context_start < i < context_end:
                diff_pos = i - context_start
                print(f"Original:    {original_context[:diff_pos]}[{original_text[i]}]{original_context[diff_pos+1:]}")
                print(f"Decompressed: {decompressed_context[:diff_pos]}[{decompressed_text[i]}]{decompressed_context[diff_pos+1:]}")
            break
    
    # Summary of potential issues
    print("\nPossible issues identified:")
    
    if len(original_lines) != len(decompressed_lines):
        print("- Different line count (line breaks not preserved)")
    
    if stripped_original != stripped_decompressed:
        print("- Different content (not just whitespace differences)")
    
    if original_chars != decompressed_chars:
        print("- Different character count")
        if decompressed_chars > original_chars:
            print("  → Decompressed file has extra characters")
        else:
            print("  → Decompressed file is missing characters")

def main():
    """Main function to process files."""
    if len(sys.argv) != 3:
        print("Usage: python compare_files.py <original_file> <decompressed_file>")
        return
    
    original_file = sys.argv[1]
    decompressed_file = sys.argv[2]
    
    if not os.path.exists(original_file) or not os.path.exists(decompressed_file):
        print("Error: File not found")
        return
    
    compare_files(original_file, decompressed_file)

if __name__ == "__main__":
    main()
