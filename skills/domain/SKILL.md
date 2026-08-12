---
name: domain
description: "When you want to brainstorm and check available .com domains for a new project — brand naming, aftermarket pricing (HugeDomains / Afternic / Sedo / Dan), USPTO trademark screening, and social handle availability. Built on Laura Roeder's \"work backwards from availability, not from a name you fell in love with\" methodology. Uses Vercel CLI + whois + Domainr API + Namecheap API + agent-browser for the pieces each tool actually reliably supports (multi-tool ensemble because no single tool covers everything cleanly). 11-step workflow: budget → brainstorm → primary availability check → whois cross-check → Domainr aggregation → Namecheap price → aftermarket sweep (+ liveness probe for parked/dead domains, drop-watch for expiring ones) → bucket → negotiate → NAME research (trademark + socials) → buy. Triggers on \"/domain,\" \"find a domain,\" \"check domain availability,\" \"brainstorm a domain,\" \"what .com is available for X,\" \"domain hunt,\" \"name my project,\" \"is X.com available,\" \"aftermarket price on X.com,\" \"trademark check for X.\""
metadata:
  version: 0.2.0
---

# /domain — Brainstorm + check available .com domains

Multi-tool workflow to find a great, affordable, available .com for a new project. Built on Laura Roeder's rule: **work backwards from what's actually available — don't fall in love with a name first** ([source](https://lauraroeder.com/how-i-nabbed-the-com-for-my-bootstrapped-startup-without-spending-a-million-bucks-6dc35c4606e9)).

Defaults to `.com` only. Only deviate (.dev, .co, .io, .ai) if the project is dev-tooling-only or the user explicitly asks.

## Step 0 — Environment checks

Verify these before proceeding (surface install commands if missing, don't try to install silently):

| Tool | Check | Install if missing |
|---|---|---|
| Vercel CLI | `vercel whoami` | `npm i -g vercel && vercel login` |
| whois | `which whois` | `brew install whois` (macOS) |
| Domainr API key | `[ -n "$DOMAINR_API_KEY" ]` | Get free key at rapidapi.com/domainr/api/domainr, add to `~/.zshenv` |
| Namecheap API | `[ -n "$NAMECHEAP_API_KEY" ] && [ -n "$NAMECHEAP_API_USER" ] && [ -n "$NAMECHEAP_CLIENT_IP" ]` | Enable API at ap.www.namecheap.com/settings/tools/apiaccess/, add 3 env vars, whitelist your IP |

Domainr + Namecheap are optional — the workflow degrades gracefully without them (skips the corresponding cross-check steps).

## Step 1 — Set the budget

Ask: **what would you pay for a great .com on this project?** Anchor defaults:

| Budget | What it buys |
|---|---|
| **$0** | Only unregistered domains (rare for anything good) |
| **$250–$1k** | Aftermarket sweet spot (HugeDomains is the standout — Laura found "a ton of great .com's available for less than $1k") |
| **$1k–$2k** | Laura's Paperbell.com range — plenty of brandable options |
| **$2k+** | Premium |

**Filter all candidates to under-budget BEFORE falling in love.**

## Step 2 — Seed words for "branded" combos

Ask what the product does + the feeling/category. Brainstorm 20–40 candidate domains using these preferences (in order):

1. **Two real words mashed together** ← preferred (Helpscout, RightMessage, ConvertKit, Paperbell, Mailchimp). Easy to spell, remember, google.
2. **Prefix/suffix the bare word** — grab the .com when the bare word is taken or over budget. "I love word X, X.com is gone, what qualifier unlocks the .com?"
   - **Modern prefixes (B2B SaaS feel)**: `try` (TryGamma, TryRoam), `use` (UseMotion, UseChalk), `with` (WithCove, WithFrame), `join` (JoinHomebase, JoinHonor)
   - **Classic prefixes (still work)**: `get` (GetMagic, GetResponse), `go` (GoCardless, GoFundMe), `hey` (HeyMarvin, HeyHenry), `the` (TheBrowserCompany, TheDyrt — editorial vibe)
   - **Dated — avoid unless intentional**: `my` (MyFitnessPal), `meet` (MeetEdgar)
   - **Suffixes**: `+ly` (Calendly, Grammarly — battle-tested but reads "2015 startup"), `+ify` (Spotify, Shopify — rare, hard to land authentically), `+labs` (AI/research positioning), `+hq` / `+app` (mostly informal)
   - **Watch**: trademark collision (`UseSlack.com` is a brand violation even if registrable); popular bare words often have `try/use/get/join` variants pre-grabbed by the same owner; longer URLs cost spelling-on-phone bandwidth
   - **Full grid**: if the user loves a bare word, generate all `try/use/with/join/get/go/hey/the + word` and `word + ly/ify/labs/hq/app` in one shot — ~15 variants
3. **One real word, slightly modified** (Trello, Pinterest, Lyft) — fine.
4. **Made-up-sounds** (Sunsama, Besedky) — only as fallback. Notoriously hard to remember.
5. **Common single-word objects** (Clubhouse, Spoke, Blush, Finder) — AVOID. Ungoogleable, .com always taken, collides with other products.

Surface a numbered candidate list before checking — don't burn cycles checking obvious losers.

## Step 3 — Primary availability check (Vercel CLI)

Use `vercel domains check` for availability and `vercel domains price` for registrar quotes. Loop candidates:

```bash
for domain in candidate1.com candidate2.com candidate3.com; do
  echo -n "$domain: "
  vercel domains check "$domain" 2>&1 | grep -E "available|not available|Error" || echo "checking..."
done
```

For pricing on the candidates that came back available:

```bash
vercel domains price candidate1.com candidate2.com candidate3.com
```

For a single deeper check on a taken domain (registrar status, expiration, nameservers if the domain is already Vercel-managed):

```bash
vercel domains inspect candidate.com
```

**TLD reliability**: Vercel CLI is rock-solid for `.com` and most gTLDs, but returns errors for `.ai`, `.dev`, `.io`, `.app` (Vercel doesn't sell those registrar-side). Skip Step 3 for non-.com candidates and go straight to Step 4.

## Step 4 — Cross-check with `whois`

Ground truth for registration status. **Query the right server per TLD** — pinning `-h whois.verisign-grs.com` to a non-.com produces silent false negatives.

**Classification order matters** (stolen from [unclaimed](https://github.com/iannuttall/unclaimed)): check for REGISTERED signals *first*, then available signals. A parked domain's whois/lander can contain "this domain is available for sale" — grepping for "available" first turns a taken name into a false positive. And **reserved ≠ available**: "is reserved", "not available for registration", "blocked for registration" all mean taken, even though RDAP often 404s these names.

- Registered signals: `creation date`, `registrar:`, `registry expiry`, `registrant`, `name server`
- Reserved signals (treat as taken): `is reserved`, `reserved by`, `not available for registration`, `blocked for registration`
- Available signals: `no match`, `not found`, `no entries found`, `no object found`, `not registered`, `available for registration`

**`.com` / `.net`** — Verisign:

```bash
for domain in candidate1.com candidate2.com; do
  result=$(whois -h whois.verisign-grs.com "$domain" 2>&1)
  if echo "$result" | grep -qiE "registrar:|creation date"; then
    expiry=$(echo "$result" | grep -i "registry expiry" | head -1 | sed 's/.*: //')
    echo "$domain → TAKEN (expires $expiry)"
  elif echo "$result" | grep -qiE "is reserved|reserved by|not available for registration|blocked for registration"; then
    echo "$domain → RESERVED (not registrable)"
  elif echo "$result" | grep -qi "no match"; then
    echo "$domain → AVAILABLE"
  else
    echo "$domain → UNKNOWN (do not treat as available)"
  fi
done
```

**Any other TLD** — don't hardcode servers; ask IANA for the authoritative whois host, then query it (`whois.nic.<tld>` is the fallback convention):

```bash
tld=ai
server=$(whois -h whois.iana.org "$tld" 2>/dev/null | grep -i "^whois:" | awk '{print $2}')
server=${server:-whois.nic.$tld}
whois -h "$server" candidate.$tld
```

Caveat: some registries have no port-43 whois at all (Google's `.dev`/`.app`/`.page` — IANA lists nothing and `whois.nic.dev` doesn't resolve). For those, RDAP below IS the ground truth.

**RDAP for `.dev` / `.app` / `.io` and other modern TLDs** — JSON-native, cleaner than whois when the TLD supports it:

```bash
UA="domain-skill/0.1 (availability check)"
for domain in candidate.dev candidate.app; do
  code=$(curl -sL -o /dev/null -w "%{http_code}" -A "$UA" "https://rdap.org/domain/$domain")
  case "$code" in
    404) echo "$domain → probably available (confirm via whois — see caveat)" ;;
    200) echo "$domain → TAKEN" ;;
    429) echo "$domain → rate-limited, sleep + retry" ;;
    *)   echo "$domain → UNKNOWN (do not treat as available)" ;;
  esac
  sleep 1  # rdap.org rate-limits aggressively
done
```

**RDAP gotchas** (all verified by the unclaimed project):
- **Always send a User-Agent** — rdap.org (and some registry servers) 403 bare requests, and a 403 read naively looks like "not 404 = taken."
- **404 ≠ proof of availability.** Registry-reserved, blocked, and premium-unsold names also 404 on RDAP. Before reporting a name available on RDAP evidence alone, confirm with a whois query (Step 4 above) — if whois says reserved, it's taken.
- **rdap.org only routes TLDs in the IANA bootstrap** (`https://data.iana.org/rdap/dns.json`). For a TLD outside it, an rdap.org 404 is meaningless — fall back to whois. Two useful direct endpoints not in the bootstrap: `.io` → `https://rdap.identitydigital.services/rdap/domain/<domain>`, `.so` → `https://rdap.nic.so/domain/<domain>`.
- A 200 body includes `events[]` — the `expiration` eventDate feeds the drop-watch in Step 7b.

**Reading the results:**
- `No match` / `no object found` / RDAP 404 (whois-confirmed) = unregistered, available
- `Registrar: <name>` / RDAP 200 = taken, check the aftermarket
- Timeout / rate-limit / weird output = **UNKNOWN — never bucket as available.** Retry later instead.

**Bulk multi-TLD sweeps** — if the hunt widens beyond a dozen candidates or beyond .com, don't hand-roll the loop; [unclaimed](https://github.com/iannuttall/unclaimed) does RDAP+whois with correct classification, resumable SQLite caching, and pricing (Node 24+):

```bash
npx unclaimed check orbit --tlds com,io,ai,dev
npx unclaimed sweep --words-file ./candidates.txt --tlds com
npx unclaimed available --sort commercial --limit 50
```

Its three states map to ours: `available` / `registered` / `unknown` (it never reports a timeout as available either).

## Step 5 — Domainr cross-check (aftermarket signal)

Domainr aggregates registrar + marketplace status across many TLDs. Skip if `DOMAINR_API_KEY` unset — otherwise:

```bash
for domain in candidate1.com candidate2.com; do
  curl -s "https://domainr.p.rapidapi.com/v2/status?domain=$domain" \
    -H "X-RapidAPI-Key: $DOMAINR_API_KEY" \
    -H "X-RapidAPI-Host: domainr.p.rapidapi.com" \
    | jq -r --arg d "$domain" '.status[] | "\($d): \(.status) — \(.summary)"'
done
```

Status codes:
- `undelegated inactive` → unregistered, free
- `active` → registered, in use
- `marketed`, `parked`, `priced` → for sale on aftermarket (Domainr surfaces price hint when available)
- `premium` → registry premium (often $500+/yr)

`marketed` or `priced` = high-signal flag to dig into HugeDomains/Afternic in Step 7.

## Step 6 — Namecheap price check

Fallback registrar — sometimes cheaper than Vercel on year-1 promo pricing. Skip if `NAMECHEAP_API_*` unset — otherwise:

```bash
DOMAINS="candidate1.com,candidate2.com,candidate3.com"
curl -s "https://api.namecheap.com/xml.response?ApiUser=$NAMECHEAP_API_USER&ApiKey=$NAMECHEAP_API_KEY&UserName=$NAMECHEAP_API_USER&Command=namecheap.domains.check&ClientIp=$NAMECHEAP_CLIENT_IP&DomainList=$DOMAINS" \
  | xmllint --xpath '//*[local-name()="DomainCheckResult"]' - 2>/dev/null \
  | grep -oE 'Domain="[^"]+" Available="[^"]+"( IsPremiumName="[^"]+")?( PremiumRegistrationPrice="[^"]+")?'
```

`Available="true"` = registrable at Namecheap registrar prices (typically $9–$15/yr for .com). `IsPremiumName="true"` = registry premium tier (skip unless under budget).

**Reconcile Vercel + Domainr + Namecheap + whois.** If they disagree (rare, happens during registrar transfers), trust `whois` for registration truth and the cheaper of Vercel/Namecheap for actual purchase.

## Step 7 — Aftermarket sweep for taken candidates

**Don't try to scrape marketplaces.** All verified failing:
- `curl` (even with realistic User-Agent) → HugeDomains 403, GoDaddy Akamai access-denied
- `WebFetch` → Cloudflare 403 across the board
- `dev-browser` skill with real Chromium → Cloudflare fingerprints Playwright automation flags, serves challenge pages. Bypassing needs `playwright-extra` + stealth plugin (flaky) or pre-warmed browser profile with human-solved captcha (not worth it for a domain hunt)
- `domainr.com` public web → IP-rate-limited
- `rdap.org` → registration status only, no aftermarket pricing

**What works**: compose marketplace URLs and have the user click. ~30 seconds per domain, 100% reliable. For every "taken" candidate the user is still curious about, output:

```
namedyoulove.com — TAKEN (Registrar: GoDaddy)
Aftermarket pricing — click to verify:
  HugeDomains: https://www.hugedomains.com/domain-profile.cfm?d=namedyoulove&e=com
  Afternic:    https://www.afternic.com/domain/namedyoulove.com
  Sedo:        https://sedo.com/search/searchresult.php4?keyword=namedyoulove.com
  Dan/GoDaddy: https://dan.com/buy-domain/namedyoulove.com
```

**Laura's HugeDomains note**: she got Paperbell.com from HugeDomains for $1,795 and recommends them as the best aftermarket starting point — "a ton of great .com's available for less than $1k." Always check HugeDomains first on taken candidates.

### Step 7a — Liveness probe: is anything actually on the taken domain?

You can't scrape the marketplaces, but you CAN fetch the taken domain itself — and its lander usually tells you where it's for sale. A taken name with no real site is also the best negotiation/outreach lead: the owner isn't using it.

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
for domain in taken1.com taken2.com; do
  body=$(curl -sL --max-time 6 -A "$UA" "https://$domain/" 2>/dev/null | head -c 16384)
  [ -z "$body" ] && body=$(curl -sL --max-time 6 -A "$UA" "http://$domain/" 2>/dev/null | head -c 16384)
  final=$(curl -sIL --max-time 6 -A "$UA" -o /dev/null -w '%{url_effective}' "https://$domain/" 2>/dev/null)
  hay="$final
$body"
  if [ -z "$body" ]; then
    echo "$domain → NONE (no DNS / dead server — best outreach lead)"
  elif echo "$hay" | grep -qiE "sedoparking|bodis\.com|parkingcrew|afternic|dan\.com|hugedomains|buy this domain|domain (name )?is for sale|domain for sale|buy now for|parked free|this web page is parked|domain has expired"; then
    marker=$(echo "$hay" | grep -oiE "sedoparking|afternic|dan\.com|hugedomains|for sale" | head -1)
    echo "$domain → PARKED ($marker — for-sale lead, note which marketplace)"
  else
    echo "$domain → LIVE (real site, owner is using it — long shot)"
  fi
done
```

(The final-URL check matters: many parked domains redirect straight to their marketplace host — e.g. landing on hugedomains.com tells you where to buy even if the lander body is JS.)

Classify each taken candidate:
- **NONE** (no DNS / connection refused) → strongest lead. Owner is squatting passively — whois-contact outreach or marketplace lowball.
- **PARKED** → for sale. The marker/redirect host tells you which marketplace to open from the Step 7 links (a HugeDomains lander = buy via HugeDomains, and the first 16KB often shows the asking price — no scraping fight needed).
- **LIVE** → in use. Drop unless the user really wants it.

Only probe taken candidates the user still cares about — it's one live request per domain.

### Step 7b — Drop-watch: taken but expiring soon

For taken candidates, Step 4 already surfaced the expiry date. gTLD post-expiry lifecycle: auto-renew grace (≤45d) → redemption (30d) → pending delete (5d), so a lapsed name drops back to the pool **~75–80 days after expiry**. Most names just get renewed — but if a candidate is NONE/PARKED *and* expiry already passed, it may genuinely be dropping:

```bash
whois -h whois.verisign-grs.com candidate.com | grep -iE "expiry|domain status"
```

- Status `redemptionPeriod` or `pendingDelete` = the owner let it lapse. Estimate drop ≈ expiry + 80 days; put a backorder in at DropCatch/SnapNames (~$59–79, pay only on catch) rather than negotiating.
- Recently-expired + parked-with-"domain has expired"-lander = same story.
- This is an "if abandoned" estimate, not a promise — recheck weekly as the date approaches.

## Step 8 — Bucket the results

Group into:
- **Available now (~$10–$30/yr)** — primary candidates
- **Aftermarket-listed under budget** — secondary (capture asking price + marketplace, from Step 7/7a)
- **Dropping soon** — lapsed per Step 7b; backorder instead of buying
- **Outreach leads** — taken, NONE/PARKED liveness, no reasonable listing; direct whois-contact offer
- **Aftermarket over budget OR live site on it** — drop

## Step 9 — Negotiate on aftermarket listings

When a candidate is listed:
- Sticker price is rarely the floor. Try a lowball 30–50% below ask.
- HugeDomains + Afternic have "Make an offer" — use it.
- If Step 7a classified the domain PARKED or NONE and the owner isn't on a marketplace, look up whois contact + offer directly. A domain with no live site for years is a motivated-seller signal — lead with a modest concrete number, not "are you interested in selling."

## Step 10 — NOW do the name research (not before!)

For top 3–5 candidates that survived availability + budget:
- Google the bare word — what else exists with it?
- Trademark check (USPTO) — see Step 10a
- Social handle availability — see Step 10b
- Say it out loud — spellable for someone on a phone call?

### Step 10a — USPTO trademark search via agent-browser

**What does NOT work** (verified — don't waste cycles):
- `curl` against tmsearch.uspto.gov → AWS WAF challenge, JS shell only, no data
- `WebFetch` against tmsearch.uspto.gov → same WAF, empty SPA shell
- `curl`/`WebFetch` against Justia, Trademarkia, TrademarkElite → all 403
- USPTO Open Data Portal API → requires USPTO.gov account linked to ID.me (hard signup)
- Marker API / RapidAPI USPTO endpoints → require key signup

**What works**: drive the real USPTO Trademark Search SPA with `agent-browser`. Angular + Material components, but the input + Enter-to-submit pattern is reliable.

```bash
# Open + search
agent-browser open "https://tmsearch.uspto.gov/" --session tm
sleep 4
agent-browser fill "#searchbar" "<phrase to check>" --session tm
agent-browser press Enter --session tm
sleep 6

# Capture results
agent-browser screenshot /tmp/tm-<slug>.png --session tm
agent-browser eval "(()=>{const m=document.body.innerText.match(/([0-9,]+)\s+results?\s+for/i); return m?m[0]:'no count';})()" --session tm
```

**Reading the result:**
- Total result count = USPTO's fuzzy/word search across the whole DB. Common words return tens of thousands — not a clearance signal on its own.
- **What matters**: scan first 5–10 visible mark names in the screenshot (or `snapshot -i | grep wordmark`). USPTO orders by relevance — an **exact-phrase match appears at the top**. If top hits are fragmentary ("MY KNOW", "KNOW MY" as separate marks), you almost certainly don't have a blocking exact-phrase registration.
- **Filter to "Live" only** in the sidebar to focus on actually-blocking marks (Dead/Cancelled don't matter for new applications).
- **Class matters**. A "GIFT ASSESSMENT" mark registered for gift-assessment services (USPTO classes 41 education, 42 SaaS, or 45 personal services) would block you. Same words in gift-baskets-class-35 might be okay.

**This is screening, not legal advice** — for any name you're seriously committing to, run past an IP lawyer or full clearance service (Cometrics/Corsearch).

```bash
agent-browser close --session tm
```

### Step 10b — Social handle availability

```bash
# X / Twitter (404 = available)
for handle in candidate1 candidate2; do
  code=$(curl -sL -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "https://x.com/$handle" --max-time 10)
  echo "  @$handle → x.com $code"
done

# LinkedIn company page (404 = available)
for handle in candidate1 candidate2; do
  code=$(curl -sL -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "https://www.linkedin.com/company/$handle" --max-time 10)
  echo "  $handle → linkedin $code"
done
```

**Instagram is unreliable from script** — IG returns 200 for any URL (SPA shell loads even for non-existent handles, "isn't available" message renders client-side). Give the user a click-through:

```
Instagram: https://instagram.com/<handle>
```

30 seconds of manual click beats fighting the IG SPA detection.

## Step 11 — Buy it

When the user picks a winner that's directly available, buy at whichever registrar quoted the lowest price in Step 3 vs Step 6:

```bash
# Vercel
vercel domains buy <domain>.com

# Namecheap (via API — uses ~/.zshenv credentials)
curl -s "https://api.namecheap.com/xml.response?ApiUser=$NAMECHEAP_API_USER&ApiKey=$NAMECHEAP_API_KEY&UserName=$NAMECHEAP_API_USER&Command=namecheap.domains.create&ClientIp=$NAMECHEAP_CLIENT_IP&DomainName=<domain>.com&Years=1&..."
```

Vercel is one-command and keeps DNS in the same dashboard as deploys — preferred unless Namecheap is meaningfully cheaper (often is on year-1 promo). Auto-renew on by default for both.

**Confirm with the user before running — this charges real money.**

For aftermarket purchases: buy through the marketplace directly (HugeDomains/Afternic/Sedo all handle escrow). Then transfer or point nameservers to Vercel after transfer completes.

## Composes with

- **`toolify`** — wire up the Domainr and Namecheap API credentials if the user hasn't yet
- **`business-brainstorm`** — pressure-test the underlying business idea BEFORE the domain hunt (a bad idea with a great .com is still a bad idea)
- **`decide`** — for the "which of the top 3 candidates" call if it's not obvious
- **`skillify`** — if the domain hunt surfaces a repeat workflow worth capturing (e.g., specific niche naming patterns), scaffold as its own sub-skill

## Notes on quality

- **Three states, always.** Every check resolves to AVAILABLE / TAKEN / UNKNOWN. A timeout, rate-limit, 403, or unparseable response is UNKNOWN — never silently bucketed as available. Retry UNKNOWNs before presenting final results.
- **Brainstorming-first, action-last.** Never run `vercel domains buy` until the user explicitly says "buy it." Real money. Availability + price checks (Step 3) use `vercel domains check` + `vercel domains price` which are safe.
- **Budget filter is non-negotiable.** If the user pushes back ("but I love it"), remind them that's exactly the trap Laura warned about.
- **Multi-tool ensemble is intentional.** No single tool covers all the bases cleanly — Vercel is fast but limited to gTLDs; whois is definitive but per-TLD-specific; Domainr aggregates; Namecheap prices year-1 promo; RDAP fills the modern-TLD gap; agent-browser drives USPTO. Skipping any leaves a blind spot.
- **Don't fight marketplace scraping.** HugeDomains/Afternic/Sedo/Dan all Cloudflare-block automation. Output click-through URLs. 30 seconds of manual click is more reliable than a headless-browser workaround.
- **USPTO screening ≠ legal clearance.** Use this for gut-check filtering; run serious names past an IP lawyer.

## Reference

Laura Roeder's original post: https://lauraroeder.com/how-i-nabbed-the-com-for-my-bootstrapped-startup-without-spending-a-million-bucks-6dc35c4606e9
