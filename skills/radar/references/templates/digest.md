# Radar — {{DATE}}

**{{RUN_TIME}}** · {{SOURCE_COUNT}} sources · {{NEW_COUNT}} new · {{CAPTURED_COUNT}} captured · {{DEGRADED_COUNT}} degraded

---

## Captured

Already in `raw/`. Nothing to do.

1. **{{TITLE}}** — ⭐️5 · {{SOURCE_NAME}} · {{AGE}}
   {{WHY_IT_CLEARED}}
   [source]({{URL}}) · `raw/{{RAW_FILE}}`

## Promotable

`/radar promote <n>` to pull any of these into `raw/` in full.

4. **{{TITLE}}** — ⭐️4 · {{SOURCE_NAME}} · {{AGE}}
   {{ONE_LINE_SUMMARY_OF_ACTUAL_SUBSTANCE}}
   [source]({{URL}})

7. **{{TITLE}}** — ⭐️3 · {{SOURCE_NAME}} · {{AGE}}
   {{ONE_LINE_SUMMARY}}
   [source]({{URL}})

## Skipped ({{SKIPPED_COUNT}})

<details>
<summary>Below the bar — titles only</summary>

- ⭐️2 {{TITLE}} · {{SOURCE_NAME}} · [link]({{URL}})
- ⭐️1 {{TITLE}} · {{SOURCE_NAME}} · [link]({{URL}})

</details>

## Source health

| Source | Status | New | Captured | Note |
|---|---|---|---|---|
| {{SOURCE_ID}} | ok | 6 | 1 | |
| {{SOURCE_ID}} | degraded | — | — | {{ERROR}} |
| {{SOURCE_ID}} | ok | 0 | 0 | nothing new in 24d — prune? |
