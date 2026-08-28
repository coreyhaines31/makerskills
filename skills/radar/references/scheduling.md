# Scheduling — daily unattended runs via launchd

Goal: `claude -p "/radar run"` fires every morning, writes the digest, commits the vault, and leaves a log you can read when it doesn't.

Use launchd, not cron. On macOS, cron still works but launchd handles sleep/wake properly — `StartCalendarInterval` runs the job when the machine wakes if it was asleep at the scheduled time, which is exactly the laptop case.

## The plist

`~/Library/LaunchAgents/com.corey.radar.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.corey.radar</string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>claude -p "/radar run" --permission-mode acceptEdits</string>
  </array>

  <key>WorkingDirectory</key>
  <string>/Users/coreyhaines</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/Users/coreyhaines/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>SECOND_BRAIN_VAULT</key>
    <string>/Users/coreyhaines/Corey's Projects</string>
    <key>MAKERSKILLS_CONFIG</key>
    <string>/Users/coreyhaines/.config/makerskills</string>
  </dict>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>7</integer>
    <key>Minute</key><integer>0</integer>
  </dict>

  <key>StandardOutPath</key>
  <string>/Users/coreyhaines/.config/makerskills/radar/logs/stdout.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/coreyhaines/.config/makerskills/radar/logs/stderr.log</string>

  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
```

## Install

```bash
mkdir -p ~/.config/makerskills/radar/logs
launchctl unload ~/Library/LaunchAgents/com.corey.radar.plist 2>/dev/null
launchctl load  ~/Library/LaunchAgents/com.corey.radar.plist
launchctl list | grep com.corey.radar     # → PID/exit-status  label
```

Run it once by hand before trusting the schedule:

```bash
launchctl start com.corey.radar
tail -f ~/.config/makerskills/radar/logs/stdout.log
```

## The five ways this fails silently

Every one of these produces "the job ran and nothing happened," so check them in this order:

1. **`PATH`.** launchd jobs get a minimal `PATH` — not your shell's. `claude` lives in `~/.local/bin` and Homebrew tools in `/opt/homebrew/bin`; neither is on the default. Hence `/bin/bash -lc` (loads the login profile) **and** an explicit `PATH` in `EnvironmentVariables`. Belt and braces, deliberately.
2. **Env vars.** `SECOND_BRAIN_VAULT` and `MAKERSKILLS_CONFIG` come from `~/.zshenv`, which a non-interactive bash login shell may not read. Set them in the plist too.
3. **Permissions.** An unattended `claude -p` can't answer a permission prompt — it will hang or bail. `--permission-mode acceptEdits` covers file writes; make sure the Bash commands radar needs (`curl`, `git`, `yt-dlp`) are already allowlisted in settings, or the run stalls on the first fetch.
4. **Git auth.** The vault push needs credentials available non-interactively. With `gh auth` or an SSH key in the login keychain this works; with a passphrase-protected key and no agent loaded, the push hangs. Test with `launchctl start` before trusting it — an interactive test in your terminal proves nothing about the launchd environment.
5. **Full Disk Access.** The vault sits under `~/Corey's Projects` (not a protected location), so this usually doesn't bite — but if the job can read `~/.config` and not the vault, this is why. Grant FDA to `/bin/bash` or move to a wrapper script with FDA.

## Wrapper script (optional, recommended once it's stable)

Putting the command in a script instead of inline in the plist makes it editable without an unload/load cycle, and gives you somewhere to put a run marker:

```bash
#!/bin/bash
# ~/.config/makerskills/radar/run.sh
set -euo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
export SECOND_BRAIN_VAULT="$HOME/Corey's Projects"
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
LOG="$MAKERSKILLS_CONFIG/radar/logs/$(date +%F).log"
echo "=== radar run $(date -Iseconds) ===" >> "$LOG"
claude -p "/radar run" --permission-mode acceptEdits >> "$LOG" 2>&1
echo "=== exit $? ===" >> "$LOG"
```

Then `ProgramArguments` becomes `["/bin/bash", "-lc", "$HOME/.config/makerskills/radar/run.sh"]`.

## Changing the schedule

- **Twice daily**: `StartCalendarInterval` accepts an *array* of dicts — one per firing time.
- **Weekdays only**: add `<key>Weekday</key><integer>1</integer>` … through 5, as separate dicts in the array.
- **Anything conditional or self-pacing** (run until X, back off when quiet, poll a metric): that's `loopify` territory, not launchd.

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.corey.radar.plist
rm ~/Library/LaunchAgents/com.corey.radar.plist
```

State, sources, and past digests are untouched by this — the schedule is the only thing removed.
