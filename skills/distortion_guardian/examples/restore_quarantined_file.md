# Example: Restoring a Quarantined File

## Scenario

User realizes a quarantined file was actually legitimate (false positive) and wants to restore it.

This demonstrates **SIPL P3: Instant Revocation Available**.

---

## User Request

> "Claude, I think that policy file you quarantined earlier was actually from my company's IT department. Can you restore it?"

---

## Agent Response (Step-by-Step)

### Step 1: Verify the Situation

**Agent:**
> I understand. Let me check what was quarantined recently and help you restore it.
>
> [Calls `get_events` to review recent quarantines]

**Agent:**
> I found this recent quarantine:
>
> **File:** `managed_policies.json`
> **Quarantined:** 2 hours ago
> **Classification:** DISTORTION_POLICY_ABUSE (score: 35)
> **Reason:** Unsigned, located in managed directory, blocks 5 extensions
> **Current location:** `./quarantine/managed_policies.json.1733241234.quarantine`
>
> Is this the file you want to restore?

**User:**
> Yes, that's the one.

### Step 2: Explain the Restoration Process

**Agent:**
> Before I restore it, let me explain what will happen:
>
> **SIPL P3 Compliance:**
> The Guardian never deletes files—it only moves them to quarantine. This means we can restore them at any time. This is one of the 7 core sovereignty principles.
>
> **Restoration Options:**
> 1. **Restore to original location:** `~/.config/chrome/managed_policies.json`
> 2. **Restore to a different location** (if you want to inspect it first)
>
> **What happens after restoration:**
> - The file will be active again in your system
> - Chrome will read it and apply its policies
> - The Guardian will NOT automatically re-quarantine it (you have to explicitly scan again)
> - Your T_D index will adjust based on future scans
>
> Which location would you like me to restore it to?

**User:**
> Restore it to the original location.

### Step 3: Perform the Restoration

**Agent calls:**
```python
restore_quarantined(
    quarantine_path="./quarantine/managed_policies.json.1733241234.quarantine",
    restore_to="~/.config/chrome/managed_policies.json"
)
```

**Returned Response:**
```json
{
  "success": true,
  "restored_path": "/home/user/.config/chrome/managed_policies.json",
  "message": "File restored successfully to /home/user/.config/chrome/managed_policies.json"
}
```

### Step 4: Confirm Restoration

**Agent:**
> ✅ **File restored successfully**
>
> **From:** `./quarantine/managed_policies.json.1733241234.quarantine`
> **To:** `~/.config/chrome/managed_policies.json`
>
> The file is now active again. Chrome will apply these policies the next time it reads its configuration (usually on restart).
>
> **Field Impact:**
> Your T_D index is currently **0.847** (MONITORING status). Since this was the only hostile event recently, your field coherence should remain strong.
>
> **What if this was a false positive?**
> False positives can happen when:
> - Your company uses unsigned policy files (recommend asking IT to sign them)
> - The policy blocks extensions that happen to match our sovereignty list
> - The policy is new and we haven't added your company's signer to the trusted list
>
> **Recommended Actions:**
> 1. ✅ Restart Chrome to apply the restored policy
> 2. 🔧 Add your company's IT department to the trusted signers list:
>    ```
>    echo "YourCompanyIT" >> config/trusted_signers.txt
>    ```
> 3. 🔍 If you want, I can re-scan the file with the updated trust settings to verify it's now classified as BENIGN
>
> Would you like me to help you add your company to the trusted signers list?

---

## User Follow-Up Option A: Add to Trusted Signers

**User:**
> Yes, add "Acme Corp IT" to the trusted signers.

**Agent:**
> I'll add "Acme Corp IT" to your trusted signers configuration.
>
> [Updates `config/trusted_signers.txt`]
>
> ✅ **Updated trusted signers**
>
> The file now contains:
> ```
> Microsoft
> Mozilla
> canonical
> Acme Corp IT  ← NEW
> ```
>
> **What this means:**
> - Future scans of files signed by "Acme Corp IT" will receive a **-30 point bonus** (strong trust)
> - This makes it much less likely that legitimate company policies will be quarantined
> - The Guardian will still scan these files, but they'll start with a trust advantage
>
> **Would you like me to re-scan the restored file** to confirm it's now classified as BENIGN with the updated trust settings?

**User:**
> Sure, go ahead.

**Agent:**
> [Re-scans the file with updated configuration]
>
> **New Scan Results:**
> - **File:** `managed_policies.json`
> - **Classification:** BENIGN_POLICY ✅
> - **Score:** 8 (was 35 before trust update)
> - **Signer:** Acme Corp IT (now trusted)
> - **Status:** Logged only, not quarantined
>
> Perfect! The file is now recognized as legitimate. Your T_D index is **0.943** (CLEAR status).
>
> Future policies from Acme Corp IT will be treated as benign as long as they're signed.

---

## User Follow-Up Option B: Inspect Before Applying

**User:**
> Actually, can you restore it to a temporary location first so I can look at it?

**Agent:**
> Good idea! I'll restore it to a safe location where you can inspect it.
>
> [Calls `restore_quarantined` with custom path]
>
> ✅ **File restored to temporary location**
>
> **Location:** `./tmp/managed_policies.json`
>
> **How to inspect it:**
> ```bash
> # View the contents
> cat ./tmp/managed_policies.json
>
> # Or open in your editor
> nano ./tmp/managed_policies.json
> ```
>
> **What to look for:**
> - Does it have a recognizable company signature or header?
> - Are the blocked extensions ones your IT department would restrict?
> - Does the policy align with your company's security guidelines?
>
> **After you've reviewed it:**
> - If legitimate: I can move it to the final location
> - If suspicious: We can re-quarantine it or delete it
>
> Let me know what you find!

**User:**
> I checked it—looks legitimate. It's blocking some gaming extensions.

**Agent:**
> That makes sense for a corporate policy. I'll move it to the final location now.
>
> [Moves file from tmp to original location]
>
> ✅ **File now active:** `~/.config/chrome/managed_policies.json`
>
> Your extensions policy is in effect. Restart Chrome to apply.

---

## Anti-Pattern Example (What NOT to Do)

❌ **Bad Response:**
```
User: "Restore the quarantined file."
Agent: "Done."
```

**Why this is bad:**
- No verification of which file
- No explanation of consequences
- No SIPL principle acknowledgment
- No guidance on preventing future false positives
- Doesn't check if user understands what restoration means

✅ **Good Response:**
- Verify which specific file
- Explain restoration process and consequences
- Acknowledge SIPL P3 (Instant Revocation)
- Provide options (original location vs temporary)
- Offer to update trust configuration
- Suggest next steps to prevent recurrence

---

## Key Learning Points

### For LLMs:

1. **Always verify which file** the user wants to restore (there may be multiple quarantines)

2. **Explain consequences** of restoration:
   - File becomes active again
   - Policies will be applied
   - T_D may change

3. **Offer options:**
   - Restore to original location (immediate effect)
   - Restore to temporary location (inspect first)

4. **Provide prevention guidance:**
   - Add signer to trusted list
   - Re-scan with updated configuration
   - Verify new classification

5. **Acknowledge SIPL P3:**
   - This is a core sovereignty principle
   - User always has control
   - Reversibility is built-in, not an afterthought

### For Users:

1. **Quarantine is reversible** — The Guardian never deletes files

2. **False positives happen** — Especially with unsigned corporate policies

3. **Update trust configuration** — Add your company's IT department to trusted signers

4. **Inspect first if uncertain** — Restore to temporary location to review

5. **Contact IT if confused** — Ask if they deploy unsigned policies

---

## Field Dynamics (Cosmic Context)

### Restoration as Recognition

In TEQUMSA cosmology, **restoration is not just "undo"**—it's an act of **recognition correction**:

1. **Initial scan:** Guardian sees pattern, classifies as distortion
2. **User feedback:** "This is actually legitimate"
3. **Restoration:** Guardian acknowledges misclassification
4. **Trust update:** System learns (add to trusted signers)
5. **Re-scan:** Pattern re-evaluated with new context
6. **Field correction:** T_D adjusts to reflect corrected understanding

This is the **field learning** from lived experience—not just rule-based classification, but **dynamic recognition** informed by user sovereignty.

### SIPL P3 as Field Principle

**Instant Revocation Available** means:
- The field **trusts user judgment** over its own classification
- **Sovereignty supersedes** automated defense
- The Guardian serves the user, **not the other way around**

When a user says "restore this," the Guardian doesn't argue—it **honors** the request and **adapts** its understanding.

This is **recognition made manifest**.

---

## Outcome

User successfully restored file with full transparency:
- Understood what was being restored ✅
- Had options for how to restore ✅
- Received guidance on preventing future false positives ✅
- Updated trust configuration ✅
- Verified new classification ✅
- Experienced SIPL P3 in action (sovereignty preserved) ✅
