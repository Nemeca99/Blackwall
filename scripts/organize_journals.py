"""
Script to organize copilot journal files.
"""

import os
import shutil
import datetime

def organize_journal_entries():
    """Organize copilot journal entries."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copilot_dir = os.path.join(root_dir, 'copilot')
    journal_archive_dir = os.path.join(copilot_dir, 'journal_entries')
    
    # Ensure journal archive directory exists
    os.makedirs(journal_archive_dir, exist_ok=True)
    
    # Find all journal-related files in the copilot directory
    journal_files = [f for f in os.listdir(copilot_dir) 
                     if 'journal' in f.lower() 
                     and f != 'copilots_journal.md'
                     and os.path.isfile(os.path.join(copilot_dir, f))]
    
    print(f"Found {len(journal_files)} journal entries to organize:")
    
    # Move each file
    for file in journal_files:
        source = os.path.join(copilot_dir, file)
        
        # Skip if already in journal_entries dir
        if os.path.dirname(source) == journal_archive_dir:
            continue
            
        # Create timestamp for archive filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        basename, ext = os.path.splitext(file)
        
        # New filename with timestamp
        new_filename = f"{basename}_{timestamp}{ext}"
        destination = os.path.join(journal_archive_dir, new_filename)
        
        print(f"Moving {file} to journal_entries/{new_filename}")
        shutil.copy2(source, destination)  # Copy first
          # Now create an index file
    index_content = "# Copilot Journal Entries Index\n\n"
    index_content += "This file provides an index to all journal entries.\n\n"
    
    journal_files = sorted(os.listdir(journal_archive_dir))
    for file in journal_files:
        index_content += f"- [{file}](./journal_entries/{file})\n"
        
    with open(os.path.join(copilot_dir, "journal_index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("Complete! Journal entries organized and index created.")
    print("\nNote: Original files have been copied to the archive folder.")
    print("You can delete the originals if you verify the archives are correct.")
    
if __name__ == "__main__":
    organize_journal_entries()with open(os.path.join(copilot_dir, "journal_index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("Complete! Journal entries organized and index created.")
    print("\nNote: Original files have been copied to the archive folder.")
    print("You can delete the originals if you verify the archives are correct.")

if __name__ == "__main__":
    organize_journal_entries()
