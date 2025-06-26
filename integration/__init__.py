"""
BlackwallV2 Integration Package

This package contains tools for integrating optimized components into the main system.
"""

from .integration_tools import (
    integrate_optimized_memory,
    integrate_optimized_fragment_routing,
    integrate_optimized_heart,
    integrate_all_optimizations,
    restore_original_components,
    view_integration_status
)

# Import media integration functions if available
try:
    from .media_integration import (
        integrate_media_enhanced_memory,
        integrate_media_aware_routing,
        integrate_all_media_components,
        restore_optimized_components
    )
    
    __all__ = [
        'integrate_optimized_memory',
        'integrate_optimized_fragment_routing',
        'integrate_optimized_heart',
        'integrate_all_optimizations',
        'restore_original_components',
        'view_integration_status',
        'integrate_media_enhanced_memory',
        'integrate_media_aware_routing',
        'integrate_all_media_components',
        'restore_optimized_components'
    ]
except ImportError:
    __all__ = [
        'integrate_optimized_memory',
        'integrate_optimized_fragment_routing',
        'integrate_optimized_heart',
        'integrate_all_optimizations',
        'restore_original_components',
        'view_integration_status'
    ]
