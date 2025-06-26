# Memory Consolidation Optimization Results

Benchmark run on: 2025-06-25T21:50:33.406596

## Summary

| Memory Count | Algorithm | Original Time (s) | Optimized Time (s) | Improvement (%) |
|--------------|----------|------------------|-------------------|----------------|
| 100 | Tag Consolidation | 0.0001 | 0.0001 | 33.67 |
| 100 | Content Consolidation | 0.0082 | 9.2326 | -112732.88 |
| 500 | Tag Consolidation | 0.0001 | 0.0001 | 1.95 |
| 500 | Content Consolidation | 0.0543 | 42.7750 | -78737.46 |
| 1000 | Tag Consolidation | 0.0003 | 0.0002 | 21.73 |
| 1000 | Content Consolidation | 0.1204 | 85.0721 | -70565.60 |


## Detailed Results

### Test with 100 memories

#### Tag Consolidation

- Original Time: 0.0001 seconds
- Optimized Time: 0.0001 seconds
- Improvement: 33.67%
- Original Consolidated Memories: 10
- Optimized Consolidated Memories: 10

#### Content Consolidation

- Original Time: 0.0082 seconds
- Optimized Time: 9.2326 seconds
- Improvement: -112732.88%
- Original Consolidated Memories: 18
- Optimized Consolidated Memories: 14

### Test with 500 memories

#### Tag Consolidation

- Original Time: 0.0001 seconds
- Optimized Time: 0.0001 seconds
- Improvement: 1.95%
- Original Consolidated Memories: 10
- Optimized Consolidated Memories: 10

#### Content Consolidation

- Original Time: 0.0543 seconds
- Optimized Time: 42.7750 seconds
- Improvement: -78737.46%
- Original Consolidated Memories: 32
- Optimized Consolidated Memories: 54

### Test with 1000 memories

#### Tag Consolidation

- Original Time: 0.0003 seconds
- Optimized Time: 0.0002 seconds
- Improvement: 21.73%
- Original Consolidated Memories: 10
- Optimized Consolidated Memories: 10

#### Content Consolidation

- Original Time: 0.1204 seconds
- Optimized Time: 85.0721 seconds
- Improvement: -70565.60%
- Original Consolidated Memories: 33
- Optimized Consolidated Memories: 151

