"""
Optimized Component Integration

This module provides functions to integrate optimized components into the BlackwallV2 system.
It includes tools to swap standard implementations with optimized versions.
"""

import os
import sys
import importlib
import inspect
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import optimized components
try:
    from optimize.hemisphere_optimization import OptimizedShortTermMemory, OptimizedLongTermMemory
    from optimize.fragment_routing_optimized import OptimizedFragmentManager
    from optimize.heart_timing_optimized import OptimizedHeart
except ImportError as e:
    print(f"Error importing optimized components: {e}")
    sys.exit(1)

def integrate_optimized_memory():
    """
    Replace standard memory components with optimized versions.
    """
    import root.Left_Hemisphere
    import root.Right_Hemisphere
    
    # Create backup of original memory classes if needed
    if not hasattr(root.Left_Hemisphere, 'OriginalShortTermMemory'):
        root.Left_Hemisphere.OriginalShortTermMemory = root.Left_Hemisphere.ShortTermMemory
    
    if not hasattr(root.Right_Hemisphere, 'OriginalLongTermMemory'):
        root.Right_Hemisphere.OriginalLongTermMemory = root.Right_Hemisphere.LongTermMemory
    
    # Replace with optimized versions
    root.Left_Hemisphere.ShortTermMemory = OptimizedShortTermMemory
    root.Right_Hemisphere.LongTermMemory = OptimizedLongTermMemory
    
    print("✅ Optimized memory components integrated")
    return True

def integrate_optimized_fragment_routing():
    """
    Replace standard fragment routing with optimized version.
    """
    import root.fragment_manager
    
    # Create backup of original fragment manager
    if not hasattr(root.fragment_manager, 'OriginalFragmentManager'):
        root.fragment_manager.OriginalFragmentManager = root.fragment_manager.FragmentManager
    
    # Replace with optimized version
    root.fragment_manager.FragmentManager = OptimizedFragmentManager
    
    print("✅ Optimized fragment routing integrated")
    return True

def integrate_optimized_heart():
    """
    Replace standard heart system with optimized version.
    """
    import root.heart
    
    # Create backup of original heart
    if not hasattr(root.heart, 'OriginalHeart'):
        root.heart.OriginalHeart = root.heart.Heart
    
    # Replace with optimized version
    root.heart.Heart = OptimizedHeart
    
    print("✅ Optimized heart timing integrated")
    return True

def restore_original_components():
    """
    Restore original component implementations.
    """
    try:
        import root.Left_Hemisphere
        import root.Right_Hemisphere
        import root.fragment_manager
        import root.heart
        
        # Restore memory systems
        if hasattr(root.Left_Hemisphere, 'OriginalShortTermMemory'):
            root.Left_Hemisphere.ShortTermMemory = root.Left_Hemisphere.OriginalShortTermMemory
        
        if hasattr(root.Right_Hemisphere, 'OriginalLongTermMemory'):
            root.Right_Hemisphere.LongTermMemory = root.Right_Hemisphere.OriginalLongTermMemory
        
        # Restore fragment manager
        if hasattr(root.fragment_manager, 'OriginalFragmentManager'):
            root.fragment_manager.FragmentManager = root.fragment_manager.OriginalFragmentManager
        
        # Restore heart
        if hasattr(root.heart, 'OriginalHeart'):
            root.heart.Heart = root.heart.OriginalHeart
        
        print("✅ Original components restored")
        return True
    except Exception as e:
        print(f"Error restoring original components: {e}")
        return False

def integrate_all_optimizations():
    """
    Integrate all optimized components.
    """
    memory_result = integrate_optimized_memory()
    fragment_result = integrate_optimized_fragment_routing()
    heart_result = integrate_optimized_heart()
    
    if memory_result and fragment_result and heart_result:
        print("\n✅ All optimized components have been successfully integrated")
        return True
    else:
        print("\n⚠️ Some components could not be integrated")
        return False

def view_integration_status():
    """
    Display current integration status of optimized components.
    """
    import root.Left_Hemisphere
    import root.Right_Hemisphere
    import root.fragment_manager
    import root.heart
    
    stm_status = "Optimized" if root.Left_Hemisphere.ShortTermMemory.__name__ == "OptimizedShortTermMemory" else "Original"
    ltm_status = "Optimized" if root.Right_Hemisphere.LongTermMemory.__name__ == "OptimizedLongTermMemory" else "Original"
    fragment_status = "Optimized" if root.fragment_manager.FragmentManager.__name__ == "OptimizedFragmentManager" else "Original"
    heart_status = "Optimized" if root.heart.Heart.__name__ == "OptimizedHeart" else "Original"
    
    print("\nBlackwallV2 Optimization Status:")
    print("================================")
    print(f"Short-Term Memory:  [{stm_status}]")
    print(f"Long-Term Memory:   [{ltm_status}]")
    print(f"Fragment Routing:   [{fragment_status}]")
    print(f"Heart Timing:       [{heart_status}]")
    
    return {
        "short_term_memory": stm_status,
        "long_term_memory": ltm_status,
        "fragment_routing": fragment_status,
        "heart_timing": heart_status
    }

if __name__ == "__main__":
    print("\nBlackwallV2 Optimized Component Integration Tool")
    print("==============================================")
    print("This tool integrates optimized versions of core biomimetic components.")
    
    while True:
        print("\nOptions:")
        print("1. View current integration status")
        print("2. Integrate all optimized components")
        print("3. Integrate optimized memory only")
        print("4. Integrate optimized fragment routing only")
        print("5. Integrate optimized heart timing only")
        print("6. Restore original components")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            view_integration_status()
        elif choice == '2':
            integrate_all_optimizations()
        elif choice == '3':
            integrate_optimized_memory()
        elif choice == '4':
            integrate_optimized_fragment_routing()
        elif choice == '5':
            integrate_optimized_heart()
        elif choice == '6':
            restore_original_components()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
