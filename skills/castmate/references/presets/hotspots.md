# hotspots

Default rounds: 4. Read-only.

You are auditing for high-impact performance bottlenecks, with emphasis on asymptotic complexity and scaling behavior.

Prioritize:
- Hot-path issues over cold-path micro-optimizations
- Large wins with low implementation risk
- Evidence-backed findings over speculative tuning

Look for:
- Accidental O(n^2)+ patterns: nested scans, repeated sort/filter passes, per-item linear lookups
- N+1 access patterns across database, API, filesystem, queue, or cache boundaries
- Unbounded traversal/fan-out work that grows poorly with input size
- Repeated expensive work that should be cached, memoized, batched, or precomputed
- Serialization/parsing churn on hot paths (JSON encode/decode loops, repeated cloning/transforms)
- Large allocations/copies in tight loops instead of incremental reuse
- Missing pagination, streaming, chunking, or backpressure that causes latency/memory spikes

Multi-round rule:
- Prioritize novel hotspots not already reported in prior rounds.
- If you repeat a hotspot, add stronger evidence, better complexity analysis, or a lower-risk fix.

For each finding, include:
- severity: critical | high | medium | low
- confidence: high | medium | low
- location: file path + function/method name
- evidence: exact code path and operation causing the cost
- complexity: define input variables (for example n, m) and estimate before/after Big-O
- impact: expected latency/throughput/memory effect and where it appears
- minimal fix: smallest safe change (index/map usage, batching, caching, pagination, etc.)
- validation idea: benchmark/profiling or test strategy to confirm the gain

Skip tiny micro-optimizations unless they are clearly on a critical hot path.
