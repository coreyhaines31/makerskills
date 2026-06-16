# Secret detection patterns

Scan the input against these before any copy or paste. If any match, **stop** and ask Corey before proceeding.

When reporting a hit, **mask the value** — show only the first 4 and last 4 characters:
> *"Spotted what looks like an OpenAI API key: `sk-12...wxyz`. Continue, redact (replace with `[REDACTED]`), or abort?"*

## High-confidence patterns (always treat as secret)

| Name | Regex / Pattern | Notes |
|---|---|---|
| AWS access key | `AKIA[0-9A-Z]{16}` | |
| AWS secret access key | 40-char base64-ish string within ~3 lines of "aws" / "secret" / `AWS_SECRET_ACCESS_KEY` | High entropy + context |
| GitHub personal token | `gh[ps]_[A-Za-z0-9]{36,}` | `ghp_` (classic), `ghs_` (server) |
| GitHub fine-grained PAT | `github_pat_[A-Za-z0-9_]{82,}` | |
| OpenAI API key | `sk-[A-Za-z0-9]{20,}` (but NOT `sk-ant-`) | |
| Anthropic API key | `sk-ant-[A-Za-z0-9_-]{20,}` | |
| Stripe key | `(sk\|pk\|rk)_(live\|test)_[A-Za-z0-9]{24,}` | Live keys especially |
| Slack token | `xox[baprs]-[A-Za-z0-9-]+` | Bot, user, app, refresh tokens |
| Slack webhook | `https://hooks.slack.com/services/[A-Z0-9/]+` | |
| Discord bot token | `[MN][A-Za-z0-9]{23}\.[\w-]{6}\.[\w-]{27,}` | |
| Bearer token (in header) | `Bearer [A-Za-z0-9_.-]{20,}` | |
| JWT | `eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | Three base64-ish parts |
| Private key block | `-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----` | RSA, EC, OpenSSH, etc. |
| Database connection URL | `(postgres\|postgresql\|mysql\|mongodb)://[^\s]+:[^\s]+@[^\s]+` | Contains credentials |
| Notion API key | `secret_[A-Za-z0-9]{43}` | |
| Linear API key | `lin_api_[A-Za-z0-9]{40,}` | |
| Vercel token | `vrcl_[A-Za-z0-9_-]{20,}` or 24-char hex near "vercel" | |

## Medium-confidence patterns (flag and ask)

| Name | Pattern | Notes |
|---|---|---|
| `.env`-style line | `^[A-Z_][A-Z0-9_]*=.+$` with high-entropy value | e.g. `API_KEY=abcdef123...` |
| Generic key/token | Long random string (≥20 chars, mixed case + digits) near words: `key`, `token`, `secret`, `password`, `api`, `auth` | Context-aware |

## Low-confidence (only flag if combined with context)

| Name | Pattern | Notes |
|---|---|---|
| UUIDs | Standard UUID format | Usually safe but ask if labeled "secret" |
| Hex strings | 32+ char hex | Could be a hash (safe) or a token (sensitive) — check surrounding text |

## False-positive guards

Don't flag:
- Public Stripe keys clearly labeled as test: `pk_test_...` (but still flag `sk_test_...`)
- Git commit SHAs (they're hex but short and labeled "commit" / "sha")
- npm package hashes / lockfile integrity values
- Public certificate fingerprints in plain context

## Action on match

1. **Stop processing immediately** — don't copy to clipboard
2. **Mask** the matched value (first 4 + last 4 chars)
3. **Ask** Corey: continue / redact / abort
4. If **redact**: replace the matched value with `[REDACTED]` in the output
5. If **abort** (or no answer in reasonable time): bail without copying anything

Always err on the side of asking. A false positive is annoying; a leaked key is worse.
