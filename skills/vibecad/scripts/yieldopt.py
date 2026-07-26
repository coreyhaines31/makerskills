#!/usr/bin/env python3
"""yieldopt — 1D cutting-stock optimizer for vibecad wood projects.

Packs a project's cut list onto purchasable stock boards (first-fit-decreasing
with kerf + end-trim allowances), then emits a shopping count, per-board cut
cards, saw-setting batches, and a yield report.

Usage:
  python3 yieldopt.py plan.json            # human-readable shop package
  python3 yieldopt.py plan.json --json     # machine-readable result

Input JSON:
{
  "kerf": 0.125,            // saw kerf per cut (default 1/8")
  "end_trim": 0.5,          // waste budgeted per board END for checked/split ends (default 0.5")
  "stock": [                // purchasable boards for ONE material (run once per material)
    {"name": "cedar 1x2 x 8ft",  "length": 96,  "price": 5.50},
    {"name": "cedar 1x2 x 12ft", "length": 144, "price": 8.50}
  ],
  "parts": [                // required pieces
    {"label": "slat A", "length": 96,  "qty": 46, "angle": "square"},
    {"label": "diag slat", "length": 144, "qty": 23, "angle": "22.5 both ends"}
  ]
}

Notes:
- Run per material/profile (don't mix 1x2 cedar with 2x4 PT in one plan).
- A part longer than every usable stock length is a hard error — resize bays
  or add a longer stock option instead of silently dropping it.
- Kerf model: kerf is charged BETWEEN retained parts. Reported offcuts are
  net of the one extra kerf needed to free them from the last part.
- Heuristic: FFD into the open board with the least usable remainder; new
  boards pick the stock with the lowest price per usable inch that fits.
  Good for typical shop plans, not provably minimal.
"""

import json
import sys


def usable(stock, end_trim):
    return stock["length"] - 2 * end_trim


def optimize(plan):
    kerf = plan.get("kerf", 0.125)
    end_trim = plan.get("end_trim", 0.5)
    stock_types = sorted(plan["stock"], key=lambda s: s["length"])
    if not stock_types:
        raise SystemExit("no stock types given")

    pieces = []
    for p in plan["parts"]:
        for _ in range(int(p.get("qty", 1))):
            pieces.append({"label": p["label"], "length": float(p["length"]),
                           "angle": p.get("angle", "square")})
    pieces.sort(key=lambda p: -p["length"])

    max_usable = max(usable(s, end_trim) for s in stock_types)
    max_raw = max(s["length"] for s in stock_types)
    too_long = [p for p in pieces if p["length"] > max_raw]
    if too_long:
        raise SystemExit(
            f"part '{too_long[0]['label']}' ({too_long[0]['length']}\") exceeds the longest "
            f"stock ({max_raw}\") — add longer stock or resize the part")

    boards = []  # {"stock":, "remaining":, "cuts": [], "whole": bool}
    # whole-board parts: longer than usable-after-trim but fit the raw board.
    # They consume a full board with NO end trim — flag them so the shopper
    # hand-picks clean-ended boards for these.
    rest = []
    for piece in pieces:
        if piece["length"] > max_usable:
            fits = [s for s in stock_types if s["length"] >= piece["length"]]
            s = min(fits, key=lambda s: s["length"])
            boards.append({"stock": s, "remaining": s["length"] - piece["length"],
                           "cuts": [piece], "whole": True})  # full-board reservation, no trim budget
        else:
            rest.append(piece)
    for piece in rest:
        need = piece["length"]
        best = None
        for b in boards:
            if b.get("whole"):
                continue
            cost = need + (kerf if b["cuts"] else 0)
            if b["remaining"] >= cost:
                leftover = b["remaining"] - cost
                if best is None or leftover < best[1]:
                    best = (b, leftover)
        if best:
            b = best[0]
            b["remaining"] -= need + (kerf if b["cuts"] else 0)
            b["cuts"].append(piece)
        else:
            fits = [s for s in stock_types if usable(s, end_trim) >= need]
            s = min(fits, key=lambda st: (st["price"] / usable(st, end_trim),
                                          usable(st, end_trim) - need))
            boards.append({"stock": s, "remaining": usable(s, end_trim) - need,
                           "cuts": [piece], "whole": False})

    return boards, kerf, end_trim


def report(plan, boards, kerf, end_trim):
    out = []
    counts, cost, bought_in, used_in = {}, 0.0, 0.0, 0.0
    for b in boards:
        n = b["stock"]["name"]
        counts[n] = counts.get(n, 0) + 1
        cost += b["stock"]["price"]
        bought_in += b["stock"]["length"]
        used_in += sum(c["length"] for c in b["cuts"])

    out.append("SHOPPING COUNT")
    for name, n in sorted(counts.items()):
        price = next(s["price"] for s in plan["stock"] if s["name"] == name)
        out.append(f"  {n:>3} x {name}  (${price:.2f} ea = ${n * price:.2f})")
    out.append(f"  material cost ${cost:.2f} | yield {100 * used_in / bought_in:.1f}%"
               f" | waste {bought_in - used_in:.1f} in"
               f" (kerf {kerf}\", end trim {end_trim}\"/end budgeted)")

    out.append("\nCUT PATTERNS (identical boards grouped — cut in listed order, longest first)")
    whole_n = sum(1 for b in boards if b.get("whole"))
    if whole_n:
        out.append(f"  NOTE: {whole_n} boards are FULL-BOARD reservations (no end-trim budget) — "
                   f"hand-pick those with clean, uncracked ends at the store")
    patterns = {}
    for b in boards:
        key = (b["stock"]["name"], b.get("whole", False),
               tuple((c["label"], c["length"]) for c in b["cuts"]))
        patterns.setdefault(key, {"n": 0, "b": b})
        patterns[key]["n"] += 1
    for (name, whole, _), v in sorted(patterns.items(), key=lambda kv: -kv[1]["n"]):
        b = v["b"]
        cuts = " | ".join(f"{c['label']} {c['length']:g}\"" for c in b["cuts"])
        tag = " FULL-BOARD" if whole else ""
        off = max(0.0, b["remaining"] - (kerf if b["remaining"] > 0 and b["cuts"] else 0))
        out.append(f"  {v['n']:>3} x [{name}]{tag}: {cuts}"
                   f"  -> offcut {off:.1f}\"")

    angles = {}
    for b in boards:
        for c in b["cuts"]:
            angles.setdefault(c["angle"], 0)
            angles[c["angle"]] += 1
    out.append("\nSAW-SETTING BATCHES (set the saw once per batch)")
    for a, n in sorted(angles.items(), key=lambda kv: (kv[0] != "square", kv[0])):
        out.append(f"  {a}: {n} cuts")

    keep = {}
    for b in boards:
        net = b["remaining"] - (kerf if b["remaining"] > 0 and b["cuts"] else 0)
        if net >= 12:
            k = round(net)
            keep[k] = keep.get(k, 0) + 1
    if keep:
        out.append("\nOFFCUTS >= 12\" worth keeping: " +
                   ", ".join(f"{n} x ~{o}\"" for o, n in sorted(keep.items(), reverse=True)))
    return "\n".join(out)


def validate_plan(plan):
    if not isinstance(plan.get("stock"), list) or not plan["stock"]:
        raise SystemExit("plan needs a non-empty 'stock' list")
    if not isinstance(plan.get("parts"), list) or not plan["parts"]:
        raise SystemExit("plan needs a non-empty 'parts' list")
    for st in plan["stock"]:
        if not (float(st.get("length", 0)) > 0 and float(st.get("price", -1)) >= 0):
            raise SystemExit(f"bad stock entry: {st}")
    plan["parts"] = [p for p in plan["parts"] if int(p.get("qty", 1)) > 0]
    for p in plan["parts"]:
        if not float(p.get("length", 0)) > 0:
            raise SystemExit(f"bad part entry (need positive length): {p}")
    if not plan["parts"]:
        raise SystemExit("no parts with qty >= 1")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    try:
        with open(args[0]) as f:
            plan = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"could not read plan: {e}")
    validate_plan(plan)
    boards, kerf, end_trim = optimize(plan)
    if "--json" in args:
        print(json.dumps({
            "boards": [{"stock": b["stock"]["name"],
                        "cuts": [{"label": c["label"], "length": c["length"],
                                  "angle": c["angle"]} for c in b["cuts"]],
                        "offcut": round(max(0.0, b["remaining"] - (plan.get("kerf", 0.125) if b["remaining"] > 0 and b["cuts"] else 0)), 2)} for b in boards],
        }, indent=2))
    else:
        print(report(plan, boards, kerf, end_trim))


if __name__ == "__main__":
    main()
