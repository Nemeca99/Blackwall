# Journal Management Script

"""
This script helps manage and remind about updates to the copilot's journal.
It can be run periodically to check when the last update was made.
"""

import os
import datetime
import time

JOURNAL_PATH = "copilot/copilots_journal.md"
REMINDER_INTERVAL_DAYS = 7  # Remind to update journal if it's been more than 7 days

def check_journal_status():
    """Check when the journal was last updated and print a reminder if needed."""
    # Get the full path to the journal
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    journal_full_path = os.path.join(base_dir, JOURNAL_PATH)
    
    if not os.path.exists(journal_full_path):
        print(f"❌ Journal not found at {journal_full_path}")
        return
    
    # Get the last modified time
    mod_time = os.path.getmtime(journal_full_path)
    mod_date = datetime.datetime.fromtimestamp(mod_time)
    current_date = datetime.datetime.now()
    days_since_update = (current_date - mod_date).days
    
    print(f"\n📔 COPILOT'S JOURNAL STATUS")
    print(f"==============================")
    print(f"Last updated: {mod_date.strftime('%Y-%m-%d %H:%M:%S')} ({days_since_update} days ago)")
    
    # Read the number of entries
    with open(journal_full_path, 'r', encoding='utf-8') as f:
        content = f.read()
        entry_count = content.count('## ')
    
    print(f"Number of entries: {entry_count}")
    
    if days_since_update > REMINDER_INTERVAL_DAYS:
        print(f"\n⚠️ REMINDER: The journal hasn't been updated in {days_since_update} days.")
        print(f"Consider adding a new entry about recent discussions and insights.")
    else:
        print(f"\n✅ Journal is up to date!")

if __name__ == "__main__":
    check_journal_status()
