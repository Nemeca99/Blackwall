#!/usr/bin/env python3
"""
Performance comparison between original and optimized memory consolidation algorithms.
"""

import os
import time
import json
import random
import argparse
from datetime import datetime
from pathlib import Path
import sys
import logging
from typing import Dict, List, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Optimization")

# Add parent directory to path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import optimized algorithms
try:
    from optimize.memory_consolidation import OptimizedMemoryConsolidation
except ImportError:
    logger.error("Could not import optimized algorithms. Make sure the optimize directory exists.")
    sys.exit(1)

# Create output directory
results_dir = os.path.join(parent_dir, "optimization_results")
os.makedirs(results_dir, exist_ok=True)


def generate_test_memories(count: int = 1000) -> List[Dict[str, Any]]:
    """Generate test memories for benchmarking."""
    logger.info(f"Generating {count} test memories...")
    
    # Define some common tags and topics for realistic data
    tags = ["memory", "thought", "observation", "insight", "concept", 
            "experience", "fact", "idea", "belief", "question"]
            
    topics = ["learning", "environment", "interaction", "communication", 
             "problem-solving", "decision-making", "creativity", "reasoning",
             "perception", "attention", "language", "emotion"]
    
    # Generate memories with somewhat realistic content patterns
    memories = []
    for i in range(count):
        tag = random.choice(tags)
        topic = random.choice(topics)
        
        # Create memory with varying complexity
        memory_content = f"This is a {tag} about {topic} "
        
        # Add some variety to create clusters of similar content
        cluster_id = i % 10  # Create 10 different clusters
        if cluster_id == 0:
            memory_content += "describing the core principles and fundamental aspects of cognitive processing."
        elif cluster_id == 1:
            memory_content += "examining how environmental factors influence learning and adaptation."
        elif cluster_id == 2:
            memory_content += "analyzing the communication patterns between different system components."
        elif cluster_id == 3:
            memory_content += "exploring creative problem-solving approaches in complex situations."
        elif cluster_id == 4:
            memory_content += "documenting observed behavioral patterns during interaction scenarios."
        else:
            # Add some random content for remaining clusters
            words = ["system", "model", "process", "structure", "function", "pattern", 
                     "behavior", "response", "stimulus", "integration", "adaptation",
                     "learning", "memory", "concept", "knowledge", "understanding"]
            memory_content += "containing " + " ".join(random.sample(words, 5))
          # Add some noise to make similarity detection more realistic
        noise_words = ["additionally", "furthermore", "however", "notably", 
                       "interestingly", "surprisingly", "evidently", "clearly",
                       "importantly", "significantly"]
        
        content_words = ["system", "model", "process", "structure", "function", "pattern", 
                     "behavior", "response", "stimulus", "integration", "adaptation",
                     "learning", "memory", "concept", "knowledge", "understanding"]
                     
        if random.random() < 0.7:  # 70% of memories get additional noise
            noise = random.choice(noise_words)
            extra_content = random.sample(content_words, 3)
            memory_content += f" {noise} this relates to {' and '.join(extra_content)}."
        
        # Create the memory object
        memories.append({
            "id": f"mem_{i}",
            "tag": tag,
            "type": "memory",
            "topic": topic,
            "content": memory_content,
            "timestamp": datetime.now().isoformat(),
            "cluster": cluster_id
        })
    
    return memories


def original_tag_consolidation(memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Reference implementation of original tag-based consolidation."""
    if not memories:
        return []
        
    # Group memories by tag
    tag_groups = {}
    for memory in memories:
        tag = memory.get('tag', '')
        if tag:
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(memory)
    
    # Consolidate memories with the same tag
    consolidated = []
    for tag, group in tag_groups.items():
        if len(group) <= 1:
            continue
            
        # Extract contents
        contents = [memory.get('content', '') for memory in group]
        combined_content = ' | '.join(contents)
        
        # Create consolidated memory
        consolidated.append({
            'id': f"consolidated_{tag}_{int(time.time())}",
            'tag': tag,
            'type': 'consolidated_memory',
            'source_count': len(group),
            'source_ids': [memory.get('id', '') for memory in group],
            'content': combined_content,
            'timestamp': time.time()
        })
        
    return consolidated


def original_content_consolidation(memories: List[Dict[str, Any]], 
                                  threshold: float = 0.5) -> List[Dict[str, Any]]:
    """Reference implementation of original content-based consolidation."""
    if not memories:
        return []
    
    # Find memories with similar content
    similarity_groups = []
    
    for i, mem1 in enumerate(memories):
        content1 = mem1.get('content', '').lower()
        if not content1:
            continue
            
        # Skip if this memory is already in a group
        if any(mem1 in group for group in similarity_groups):
            continue
            
        # Find similar memories
        similar_mems = [mem1]
        words1 = set(content1.split())
        
        for j, mem2 in enumerate(memories):
            if i == j:
                continue
                
            content2 = mem2.get('content', '').lower()
            if not content2:
                continue
                
            # Calculate Jaccard similarity
            words2 = set(content2.split())
            if not words1 or not words2:
                continue
                
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            
            similarity = intersection / union if union > 0 else 0
            
            if similarity >= threshold:
                similar_mems.append(mem2)
                
        # Add group if multiple memories are similar
        if len(similar_mems) > 1:
            similarity_groups.append(similar_mems)
    
    # Create consolidated memories from similarity groups
    consolidated = []
    for group in similarity_groups:
        # Extract contents and tags
        contents = [memory.get('content', '') for memory in group]
        tags = set()
        for memory in group:
            tag = memory.get('tag', '')
            if tag:
                tags.add(tag)
        
        # Join related contents
        combined_content = ' | '.join(contents)
        
        # Create consolidated memory
        consolidated.append({
            'id': f"consolidated_content_{int(time.time())}",
            'tag': ','.join(tags) if tags else 'consolidated',
            'type': 'consolidated_memory',
            'source_count': len(group),
            'source_ids': [memory.get('id', '') for memory in group],
            'content': combined_content,
            'timestamp': time.time()
        })
        
    return consolidated


def run_benchmark(memory_counts: List[int] = [100, 500, 1000, 5000]) -> Dict[str, Any]:
    """
    Run benchmark comparing original and optimized algorithms.
    
    Args:
        memory_counts: List of memory counts to test
        
    Returns:
        Dictionary with benchmark results
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": []
    }
      # Create optimized consolidation instance
    optimized = OptimizedMemoryConsolidation(similarity_threshold=0.7)  # Higher threshold for better precision
    
    for count in memory_counts:
        logger.info(f"Benchmarking with {count} memories...")
        test_memories = generate_test_memories(count)
        
        # Benchmark tag consolidation
        logger.info("Testing tag consolidation...")
        
        # Original implementation
        start_time = time.time()
        original_tag_results = original_tag_consolidation(test_memories)
        original_tag_time = time.time() - start_time
        logger.info(f"Original tag consolidation: {original_tag_time:.4f}s, {len(original_tag_results)} consolidated memories")
        
        # Optimized implementation
        start_time = time.time()
        optimized_tag_results = optimized.consolidate_by_tag(test_memories)
        optimized_tag_time = time.time() - start_time
        logger.info(f"Optimized tag consolidation: {optimized_tag_time:.4f}s, {len(optimized_tag_results)} consolidated memories")
        
        # Improvement percentage
        tag_improvement = (1 - (optimized_tag_time / original_tag_time)) * 100 if original_tag_time > 0 else 0
        logger.info(f"Tag consolidation improvement: {tag_improvement:.2f}%")
        
        # Benchmark content consolidation
        logger.info("Testing content consolidation...")
        
        # Original implementation
        start_time = time.time()
        original_content_results = original_content_consolidation(test_memories)
        original_content_time = time.time() - start_time
        logger.info(f"Original content consolidation: {original_content_time:.4f}s, {len(original_content_results)} consolidated memories")
        
        # Optimized implementation
        start_time = time.time()
        optimized_content_results = optimized.consolidate_by_content(test_memories)
        optimized_content_time = time.time() - start_time
        logger.info(f"Optimized content consolidation: {optimized_content_time:.4f}s, {len(optimized_content_results)} consolidated memories")
        
        # Improvement percentage
        content_improvement = (1 - (optimized_content_time / original_content_time)) * 100 if original_content_time > 0 else 0
        logger.info(f"Content consolidation improvement: {content_improvement:.2f}%")
        
        # Store results
        test_result = {
            "memory_count": count,
            "tag_consolidation": {
                "original_time": original_tag_time,
                "optimized_time": optimized_tag_time,
                "improvement_percent": tag_improvement,
                "original_count": len(original_tag_results),
                "optimized_count": len(optimized_tag_results)
            },
            "content_consolidation": {
                "original_time": original_content_time,
                "optimized_time": optimized_content_time,
                "improvement_percent": content_improvement,
                "original_count": len(original_content_results),
                "optimized_count": len(optimized_content_results)
            }
        }
        results["tests"].append(test_result)
        
    return results


def save_results(results: Dict[str, Any]) -> str:
    """Save benchmark results to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"optimization_results_{timestamp}.json")
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    # Also create a markdown summary
    summary_file = os.path.join(results_dir, f"optimization_summary_{timestamp}.md")
    
    with open(summary_file, 'w') as f:
        f.write("# Memory Consolidation Optimization Results\n\n")
        f.write(f"Benchmark run on: {results['timestamp']}\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Memory Count | Algorithm | Original Time (s) | Optimized Time (s) | Improvement (%) |\n")
        f.write("|--------------|----------|------------------|-------------------|----------------|\n")
        
        for test in results["tests"]:
            count = test["memory_count"]
            
            # Tag consolidation
            tag_orig = test["tag_consolidation"]["original_time"]
            tag_opt = test["tag_consolidation"]["optimized_time"]
            tag_imp = test["tag_consolidation"]["improvement_percent"]
            f.write(f"| {count} | Tag Consolidation | {tag_orig:.4f} | {tag_opt:.4f} | {tag_imp:.2f} |\n")
            
            # Content consolidation
            cont_orig = test["content_consolidation"]["original_time"]
            cont_opt = test["content_consolidation"]["optimized_time"]
            cont_imp = test["content_consolidation"]["improvement_percent"]
            f.write(f"| {count} | Content Consolidation | {cont_orig:.4f} | {cont_opt:.4f} | {cont_imp:.2f} |\n")
        
        f.write("\n\n## Detailed Results\n\n")
        
        for test in results["tests"]:
            count = test["memory_count"]
            f.write(f"### Test with {count} memories\n\n")
            
            f.write("#### Tag Consolidation\n\n")
            f.write(f"- Original Time: {test['tag_consolidation']['original_time']:.4f} seconds\n")
            f.write(f"- Optimized Time: {test['tag_consolidation']['optimized_time']:.4f} seconds\n")
            f.write(f"- Improvement: {test['tag_consolidation']['improvement_percent']:.2f}%\n")
            f.write(f"- Original Consolidated Memories: {test['tag_consolidation']['original_count']}\n")
            f.write(f"- Optimized Consolidated Memories: {test['tag_consolidation']['optimized_count']}\n\n")
            
            f.write("#### Content Consolidation\n\n")
            f.write(f"- Original Time: {test['content_consolidation']['original_time']:.4f} seconds\n")
            f.write(f"- Optimized Time: {test['content_consolidation']['optimized_time']:.4f} seconds\n")
            f.write(f"- Improvement: {test['content_consolidation']['improvement_percent']:.2f}%\n")
            f.write(f"- Original Consolidated Memories: {test['content_consolidation']['original_count']}\n")
            f.write(f"- Optimized Consolidated Memories: {test['content_consolidation']['optimized_count']}\n\n")
    
    logger.info(f"Results saved to {results_file}")
    logger.info(f"Summary saved to {summary_file}")
    
    return summary_file


def main():
    """Run the optimization benchmark."""
    parser = argparse.ArgumentParser(description='Memory consolidation optimization benchmark')
    parser.add_argument('--counts', type=int, nargs='+', default=[100, 500, 1000, 2000],
                        help='Memory counts to test')
    args = parser.parse_args()
    
    logger.info("Starting memory consolidation optimization benchmark...")
    
    # Run benchmark
    results = run_benchmark(args.counts)
    
    # Save results
    summary_file = save_results(results)
    
    logger.info(f"Benchmark complete. Results saved to {summary_file}")


if __name__ == "__main__":
    main()
