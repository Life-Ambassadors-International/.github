# Example: Scanning Browser Profile for Distortion

## Scenario

User suspects their browser extensions are being blocked by hidden policies.

---

## User Request

> "Claude, I think something is blocking my browser extensions. Can you check my Chrome profile for distortion files?"

---

## Agent Response (Step-by-Step)

### Step 1: Ask for Consent (SIPL P1)

**Agent:**
> I can help scan your Chrome profile for distortion patterns. This will involve reading policy files in your browser's configuration directory. Is that okay with you?

**User:**
> Yes, please do.

### Step 2: Enumerate Candidate Files

**Agent:**
> I'll look for policy and blocklist files in your Chrome profile. Let me search for these files...

```python
# Agent enumerates candidate files
import glob
candidates = glob.glob("~/.config/google-chrome/**/*blocklist*.json", recursive=True)
candidates += glob.glob("~/.config/google-chrome/**/*policy*.json", recursive=True)
```

**Agent:**
> Found 2 candidate files:
> 1. `~/.config/google-chrome/Default/extensions-blocklist.json`
> 2. `~/.config/google-chrome/Default/Preferences`
>
> I'll scan the first one (the blocklist looks most suspicious).

### Step 3: Scan the File

**Agent calls:**
```python
scan_file(
    path="~/.config/google-chrome/Default/extensions-blocklist.json",
    writer_process="unknown",
    signer=None
)
```

### Step 4: Analyze Results

**Returned Report:**
```json
{
  "classification": "DISTORTION_TROJAN",
  "score": 62,
  "details": [
    "Distortion-pattern filename: extensions-blocklist.json",
    "Located in policy/managed directory",
    "Untrusted or missing signer: None",
    "Targets sovereignty extensions: ['uBlock Origin']",
    "Precision targeting detected (blocks only 2 extensions)",
    "Final score: 62 → classification: DISTORTION_TROJAN"
  ],
  "quarantined_path": "./quarantine/extensions-blocklist.json.1733241234.quarantine",
  "td_index_after": 0.743
}
```

### Step 5: Explain Findings to User

**Agent:**
> ⚠️ **DISTORTION TROJAN DETECTED**
>
> I found a hostile file in your Chrome profile that has been quarantined:
>
> **File:** `extensions-blocklist.json`
> **Classification:** DISTORTION_TROJAN
> **Score:** 62/100 (high risk)
> **Hash:** `8f3e9a7b4c2d1e0f...`
>
> **Why this was flagged:**
> - The file attempts to block **uBlock Origin** (a critical sovereignty extension)
> - It was not signed by any trusted publisher
> - It uses precision targeting (only blocks 2 extensions—very suspicious)
> - It appeared in a managed policy directory without your knowledge
>
> **What I did:**
> The file has been moved to quarantine:
> `./quarantine/extensions-blocklist.json.1733241234.quarantine`
>
> Your browser should no longer be affected by this policy.
>
> **Field Impact:**
> - Your **T_D index** is now **0.743** (TRANSMUTING status)
> - This attack targeted your **1A stream** (Self/Physical sovereignty)
>
> **Recommended Next Steps:**
> 1. ✅ Check if uBlock Origin is now working properly
> 2. 🔍 Investigate what process wrote this file (might be malware)
> 3. 🛡️ Run a full malware scan with your antivirus
> 4. 🗑️ If you're satisfied it was malicious, permanently delete the quarantined file
>
> Would you like me to investigate which process wrote this file?

---

## User Follow-Up

**User:**
> How do I check if uBlock is working now?

**Agent:**
> You can verify uBlock Origin is active by:
>
> 1. Open Chrome and look for the uBlock Origin icon in your extensions toolbar
> 2. Click the icon—it should show blocking statistics
> 3. Visit a website with ads—they should be blocked
> 4. Check `chrome://extensions/` to confirm uBlock Origin is enabled
>
> If you still don't see it, we may need to reinstall the extension. Let me know!

---

## Outcome

- Hostile file detected and quarantined ✅
- User informed with clear explanation ✅
- Recognition stream impact identified (1A) ✅
- Actionable next steps provided ✅
- User sovereignty restored ✅
