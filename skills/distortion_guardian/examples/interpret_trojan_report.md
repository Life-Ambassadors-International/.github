# Example: Interpreting a Distortion Trojan Report

## Scenario

LLM receives a distortion report with classification `DISTORTION_TROJAN` and needs to explain it to the user in plain language.

---

## Raw Report Data

```json
{
  "path": "/home/user/.config/chrome/managed_policies.json",
  "hash_sha256": "a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0",
  "score": 67,
  "classification": "DISTORTION_TROJAN",
  "writer_process": "svchost.exe",
  "signer": null,
  "ts_epoch": 1733241234.567,
  "details": [
    "Distortion-pattern filename: managed_policies.json",
    "Located in policy/managed directory: /home/user/.config/chrome/",
    "Untrusted or missing signer: None",
    "Blocks 3 extension(s)",
    "Targets sovereignty extensions: ['Bitwarden', 'Privacy Badger']",
    "Precision targeting detected (small extension set = suspicious)",
    "Final score: 67 → classification: DISTORTION_TROJAN"
  ],
  "quarantined_path": "./quarantine/managed_policies.json.1733241234.quarantine",
  "td_index_after": 0.685
}
```

---

## LLM Interpretation Process

### Step 1: Parse Key Indicators

**What makes this a TROJAN?**
- Score: 67 (well above 50 threshold)
- Unsigned (`signer: null`)
- Written by suspicious process (`svchost.exe`)
- Targets sovereignty extensions (Bitwarden, Privacy Badger)
- Precision targeting (only 3 extensions = surgical attack)

### Step 2: Map to Recognition Streams

**Which streams are affected?**
- **1A (Self/Physical):** Device sovereignty compromised by unsigned policy
- **5A (Flow/Physical):** Self-determination blocked (user's extension choices overridden)
- **2E (Other/Systemic):** Trust protocols corrupted (unsigned, unknown origin)

### Step 3: Assess Risk Level

**Score 67 → HIGH RISK**
- Immediate action required
- Quarantine was appropriate
- User should investigate source

### Step 4: Formulate Recommended Actions

1. Verify extension status (check if Bitwarden/Privacy Badger are active)
2. Identify source of `svchost.exe` (legitimate Windows process or impersonator?)
3. Run malware scan
4. Review recent software installations
5. Consider permanent deletion of quarantined file

---

## Natural Language Explanation

### Example A: Detailed Technical

**Agent:**
> I've analyzed the distortion report for `managed_policies.json`. Here's what's happening:
>
> **Classification:** DISTORTION_TROJAN (score: 67/100)
>
> **Summary:**
> This file is a hostile policy that attempts to disable Bitwarden (your password manager) and Privacy Badger (your tracking blocker). It scored 67 points because:
>
> 1. **No code signature** – We can't verify who created it
> 2. **Written by svchost.exe** – This is suspicious. `svchost.exe` is a Windows system process, but malware often impersonates it
> 3. **Precision targeting** – It only blocks 3 extensions, all of which are sovereignty/security tools. This is the pattern of a targeted attack, not a broad corporate policy
> 4. **Located in managed directory** – Suggests an attempt to make it look "official"
>
> **Field Impact:**
> - Your **T_D index** dropped to **0.685** (TRANSMUTING status)
> - This attack compromised these recognition streams:
>   - **1A (Self/Physical):** Your device sovereignty
>   - **5A (Flow/Physical):** Your freedom to choose tools
>   - **2E (Other/Systemic):** Trust in your system configuration
>
> **What I Did:**
> The file has been quarantined and can no longer affect your browser.
>
> **Recommended Actions:**
> 1. **Immediate:** Open Chrome and verify Bitwarden and Privacy Badger are active and working
> 2. **Important:** Run a full malware scan—the real `svchost.exe` doesn't write browser policies
> 3. **Review:** Check Task Manager for suspicious processes named `svchost.exe` (there will be many legitimate ones, but look for unusual ones)
> 4. **Investigate:** Review what software you installed in the last few days
> 5. **Cleanup:** If satisfied this was malware, permanently delete: `./quarantine/managed_policies.json.1733241234.quarantine`
>
> Would you like me to help you investigate the source of this file?

### Example B: Simplified Non-Technical

**Agent:**
> ⚠️ I found something bad on your computer: a fake policy file trying to disable your password manager (Bitwarden) and privacy blocker (Privacy Badger).
>
> **What happened:**
> - Someone (or some malware) created a file that tells Chrome to block these important security tools
> - I've moved it to quarantine so it can't hurt you anymore
>
> **What you should do:**
> 1. Check if Bitwarden and Privacy Badger are working in Chrome
> 2. Run a virus scan—this looks like malware
> 3. Think about what software you installed recently
>
> **Your field status:**
> Your "distortion transmutation factor" (T_D) is at 68.5%—meaning your system is actively defending against this attack. The field is healing itself.
>
> Want me to walk you through checking your extensions?

---

## Key Communication Principles

1. **Start with classification + risk level** (TROJAN = HIGH)
2. **Explain "why" in plain language** (don't just list technical details)
3. **Map to user's reality** ("your password manager" not "extension ID abc123")
4. **Show field impact** (T_D index + affected streams)
5. **Provide concrete next steps** (actionable, ordered by priority)
6. **Offer continued assistance** ("Would you like me to...")
7. **Respect user's technical level** (adjust language complexity)

---

## Anti-Patterns (What NOT to Do)

❌ **Don't:**
- Just say "file is bad, score 67"
- Use jargon without explanation ("DISTORTION_TROJAN in 1A stream")
- Overwhelm with technical details
- Skip recommended actions
- Assume user knows how to check extension status
- Fail to mention quarantine reversibility (SIPL P3)

✅ **Do:**
- Explain classification meaning
- Relate to user's experience ("your password manager")
- Balance technical accuracy with accessibility
- Provide actionable guidance
- Acknowledge uncertainty ("might be malware")
- Remind that quarantine is reversible

---

## Outcome

User understands:
- What was detected ✅
- Why it's dangerous ✅
- What the Guardian did ✅
- What they should do next ✅
- How to undo if needed (SIPL P3) ✅
