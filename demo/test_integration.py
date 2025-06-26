"""
BlackwallV2 Integration Test

This script tests that all modules have been properly integrated and can be imported.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import all components from the root package
try:
    from BlackwallV2.Implementation.root import (
        Anchor,
        Body,
        Brainstem,
        Ears,
        Eyes,
        Hands,
        Heart,
        ShortTermMemory,
        Lungs,
        Mirror,
        Mouth,
        Nerves,
        LongTermMemory,
        Shield,
        Skin,
        Soul,
        Spine
    )
    print("✅ Successfully imported all BlackwallV2 components")
    
    # Test instantiating key components
    body = Body()
    print("✅ Created Body instance")
    
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    print("✅ Created memory components")
    
    soul = Soul()
    print("✅ Created Soul instance")
    
    brainstem = Brainstem()
    print("✅ Created Brainstem instance")
    
    print("\nAll components successfully integrated!")
    
except Exception as e:
    print(f"❌ Error during import test: {e}")
    import traceback
    traceback.print_exc()
