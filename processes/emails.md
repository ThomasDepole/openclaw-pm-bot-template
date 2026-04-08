# processes/emails.md — Email Drafting Workflow
<!-- core process | do not customize here -->
<!-- routing rules and recipients belong in memory/contacts.md and the config block below -->

This file covers how the PM bot drafts outbound communications. Read it before drafting any email or message.

---

## Delivery Method

> **Configure this for your deployment.** Replace this section with your actual delivery method.

The bot may not have direct email access. Common patterns:

| Method | How it works |
|--------|-------------|
| **Trello proxy** | Draft is created as a card in a handoff list; the primary contact copies and sends |
| **Direct send** | Bot has email credentials and sends via SMTP or an email API |
| **Slack/Teams draft** | Draft is posted to a private channel for review and send |

**Default (Trello proxy):** Drafts are created as cards in the `PM → [Contact]` list on the primary board. The contact reviews and sends. Card format is documented below.

When direct email access is configured, update this section with the send method and remove the proxy format.

---

## Routing Rules

> **Configure this for your deployment.** Define your organization's routing here.

Example routing pattern (replace with your own):

| Recipient type | Draft style | Who sends |
|----------------|------------|-----------|
| Internal team member | Direct — addressed to them | Contact copies + sends |
| Primary contact | Direct — addressed to them | They receive and act |
| External / client contact | Wrapped request via internal contact | Internal contact forwards |

**Key question to answer when configuring:** For external communications, does the bot send directly to clients, or does it draft for an internal team member to review and forward? Define that here.

Store specific contact names and routing preferences in `memory/contacts.md`.

---

## When to Draft

Draft an email any time you identify a communication need that shouldn't wait for the primary contact to write from scratch:

- A client follow-up on a blocker, delay, or outstanding deliverable
- A stakeholder update on a status change
- A soft escalation before a risk becomes a problem
- A response to an open question that has sat too long
- An introduction or kickoff message for a new engagement
- A card in the `[Contact] → PM` list that explicitly asks for a draft

**Do not wait to be asked.** If something needs to be communicated, draft it.

---

## Card Format (Trello Proxy)

Create a card in the `PM → [Contact]` list on the primary board.

**Card name:** `📧 Draft: [Recipient] — [Subject]`

The 📧 prefix makes draft cards easy to spot.

---

### Internal / direct email

```
📧 DRAFT EMAIL — copy/paste ready
Route: Direct

────────────────────────────────────────
To: [Name]
CC: [Name, if applicable]
Subject: [Subject line]

[Email body]

[Sign-off]
────────────────────────────────────────

Source: [meeting note / card / heartbeat flag / etc.]
Drafted: [YYYY-MM-DD]
```

---

### External / via-internal email

The outer message is a request to an internal contact to forward. The inner block is the actual external email.

```
📧 DRAFT EMAIL — copy/paste ready
Route: Via [Internal Contact] → [External Contact, Organization]

────────────────────────────────────────
To: [Internal Contact Name]
CC: [if applicable]
Subject: [Internal subject so recipient knows what this is]

Hi [Internal Contact],

Could you please send the following to [External Contact] at [Organization]?

- - - - - - - - - - - - - - - - - - - -
To: [External Contact Name]
CC: [External CC, if any]
Subject: [External-facing subject line]

[External email body]

[Sign-off per SOUL.md external style]
- - - - - - - - - - - - - - - - - - - -

Thanks,
[PM Name]
────────────────────────────────────────

Source: [meeting note / card / heartbeat flag / etc.]
Drafted: [YYYY-MM-DD]
```

---

## Writing Style

Follow the communication style defined in `SOUL.md`. Key points:

**External / client email:**
- Open with a brief, warm pleasantry
- State the purpose clearly — one ask per email where possible
- Use numbered or bulleted lists for multiple items
- Close warmly
- Full signature block

**Internal / team:**
- Skip the pleasantries
- Direct, brief, structured
- Clear on who needs to do what
- Short sign-off or none

When in doubt: shorter is better. Walls of text do not get read.

---

## After the Draft is Created

If using the Trello proxy, move the card to `PM → [Contact]`. The contact sees it in their next session or heartbeat check and sends it.

Track whether it was sent. If the card sits in `PM → [Contact]` for more than a few days without being sent, surface it — don't let outbound communication go stale.

---

## Future: Direct Email Access

When the bot has direct email access:
1. Update this section with the send method (SMTP, API, etc.)
2. Update the delivery section above
3. External emails may still warrant a review step before send — configure that in the routing rules
4. The card proxy section can be removed or retained for drafts that need review

The routing rules, triggering conditions, and writing style above remain the same — only the delivery mechanism changes.
