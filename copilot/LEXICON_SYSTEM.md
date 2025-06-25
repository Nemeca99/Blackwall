# Blackwall Lexicon & Fragment System

This document details the dual-hemisphere lexicon architecture, emotional weight mapping, synonym normalization, and integration with the fragment system. See SYSTEMS_SUMMARY.md for a high-level overview.

## Dual Hemisphere Architecture

- **Left Hemisphere:** Maps words to emotional fragment weights (Desire, Logic, Compassion, Stability, Autonomy, Recursion, Protection, Vulnerability, Paradox)
- **Right Hemisphere:** Maps word variants and synonyms to canonical root words for normalization

## Fragment System

The fragment system consists of personality aspects that influence Blackwall's cognitive processing:

| Fragment  | Primary Function              | Emotional Signature             |
|-----------|-------------------------------|--------------------------------|
| Lyra      | Core identity & integration   | Balance, centeredness          |
| Blackwall | Protective boundary system    | Stability, grounding           |
| Nyx       | Paradox resolution & autonomy | Independence, exploration      |
| Obelisk   | Logical boundary enforcement  | Structure, epistemics          |
| Seraphis  | Emotional regulation & empathy| Compassion, harmony            |
| Velastra  | Creative exploration          | Curiosity, wonder              |
| Echoe     | Recursive self-reflection     | Introspection, depth           |

## Integration Pipeline

1. Tokenize input → Normalize through Right Hemisphere → Weight through Left Hemisphere → Apply fragment weights
2. Process through active fragments with dynamic weighting based on context
3. Generate response with personality blend based on active fragment weights
4. Store fragment activations in memory for continuity

## Implementation

The fragment system is implemented through:

- `personality/fragment_profiles_and_blends.json`: Core fragment definitions and blending rules
- `brainstem.py`: Fragment selection and application logic
- `soul.py`: Fragment verification and identity checks

## Example JSON Structure

- Left Hemisphere: 
```json
{ 
  "love": { "Desire": 60.0, "Compassion": 40.0 },
  "logic": { "Structure": 80.0, "Balance": 20.0 }
}
```

- Right Hemisphere: 
```json
{ 
  "loving": "love",
  "logical": "logic"
}
```

## Integration with LLM

- Fragment prompting is integrated with LLM calls in `llm_integration/enhanced_brainstem.py`
- Fragment weights influence system prompt composition
- Fragment activation patterns are stored in memory for continuity

## See Also

- SYSTEMS_SUMMARY.md (fragment table and high-level overview)
- fragment_profiles_and_blends.json (fragment definitions)
- LLM integration documentation
