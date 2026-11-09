# Performance: broken → baseline → limiter → change → remeasure

If **front-end-performance-audit**, **back-end-performance-audit** or **database-performance-audit** are installed, use them for depth. They're separate skills, not part of makerskills. If they're missing, use this file and say the specialist wasn't available.

## Order of operations

1. **Broken before slow.** A failing critical path outranks any speedup.
2. **Baseline.** Name the journey, environment and build, device or hardware, network and region, dataset and tenant size, load, cold vs warm, sample count and window. Decide up front what result would change your decision.
3. **Find the limiter.** Prefer existing traces and telemetry. New load tests need request, concurrency, time and spend ceilings, plus stop conditions.
4. **Rank** by benefit vs cost and risk. Get the user's pick before changing anything.
5. **Remeasure comparably.** Report faster, slower, no measurable difference, or inconclusive, with counts and spread.

Static recommendations are hypotheses. Compare equivalent completed work: a faster failure or "job enqueued" isn't a win. **Fewer tests isn't a speedup.** Don't average percentiles. Don't count a DB fix again as a backend saving.

## Frontend

Keep field and lab data separate. For the web, look at LCP, INP and CLS plus the waterfall, the actual LCP element, long tasks, layout shifts, asset and font sizes, JS execution, hydration and third parties. Lighthouse TBT isn't real-user INP. Measure time to useful content, not time to a spinner. Don't lazy-load the hero image or preload everything. For native apps, measure startup and resume, input-to-display, hitches, memory and power, not a web score.

## Backend

Trace p50/p95/p99 with real sample sizes. Look at errors, successful throughput, CPU, memory, GC and event loop, dependency latency, pool waits, and queue depth and age. Concurrent spans don't add up like serial ones. Look for serial calls, repeated computation, oversized payloads, retries and unbounded work. More parallelism can overload what's downstream, so check pool and provider limits first.

## Database

Count actual queries, rows, bytes, pool and lock waits. One ORM call can issue many statements. Replacing an N+1 with one enormous join can be worse. Compare projections, bounded eager loads, cursor pagination, composite or partial indexes, and transaction scope against real predicates and plans. Sequential scans aren't automatically bad, and indexes cost writes.

**EXPLAIN ANALYZE executes the query.** Rolling back doesn't undo every side effect. Don't run it against production writes without explicit approval. Plain EXPLAIN gives estimates, not elapsed time. Check the installed Prisma, driver and database versions before giving API or settings advice.

## Cache contract: fill this in before recommending a cache

- Owner / source of truth / measured repeated work
- Layer (request, browser, client, CDN, framework, app)
- Sensitivity and audience (request-local / per-user / per-tenant / public)
- **Complete key:** tenant, user or policy revision where results differ, query, locale, schema version
- **Authorization still checked on every hit**
- TTL rationale and acceptable staleness
- Invalidation on write, delete, permission change and account switch
- Race between a slow old fill and an invalidation (generation or version check)
- Miss, error and outage fallback (never fail open)
- Stampede protection, capacity, eviction, cost
- Isolation and freshness tests, bypass and rollback owner

TTL alone can't satisfy immediate revocation. Shared CDN caching needs demonstrably public content and verified headers.

**Next.js:** check the installed version, router, runtime and Cache Components setting first. Render memoization, fetch caching, the data cache, the router cache and the CDN are different layers. Don't assume fetch auto-caches, or that process memory survives between serverless invocations. Never force personalized content static to win a score.

### Example (synthetic): project summary cache

**Bad:** key = project ID; cached 24h on a shared CDN; the payload includes internal notes. A tenant-ID key still fails when members and clients see different views.

**Good:** auth is checked at the request boundary on every hit. Cache per tenant and audience, and only after measuring repeated work. Key on schema version, tenant, project, policy revision, locale and filters. Invalidate after successful writes using a generation check. A revoked user is denied even if the cached object still exists. On cache outage, fall back to an authorized source read with backpressure.

Tests: warm as admin → read as client (client-safe view only) → read as another tenant with forged IDs (deny) → revoke admin and reuse the session (deny) → edit and confirm freshness → race a slow fill against an invalidation → simulate an outage → measure hit and miss times before and after.

## Report format

Finding → evidence (ref, window) → limiter or hypothesis → affected journey → confidence → estimated or actual benefit → cost and risk → proposed change → proof and rollback. Lab proof isn't production proof.
