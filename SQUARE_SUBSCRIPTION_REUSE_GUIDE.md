# Square Subscription Reuse Guide

This document explains how the subscription payment flow is implemented in this project using Square, so you can reuse it in other Django projects.

## 1) What This Implementation Includes

- Card checkout with Square Web Payments SDK on the frontend.
- Backend payment creation through Square Python SDK.
- Customer lookup/create in Square before charging.
- Optional card-on-file save after successful payment.
- Subscription activation in Django (`pro` / `one-year`).
- Admin renewal-link generation and sending.

Primary files in this project:

- `myproject/settings.py`
- `myapp/views.py`
- `myapp/urls.py`
- `myapp/models.py`
- `myapp/templates/myapp/aibots/settings/upgrade_to_pro.html`
- `myapp/admin_urls.py`
- `myapp/templates/myapp/aibots/admin/renewal.html`

---

## 2) Dependencies

`requirements.txt` contains:

- `squareup==37.1.1.20240717`

Install in new projects:

```bash
pip install squareup
```

---

## 3) Environment Variables

Add these to `.env`:

```env
SQUARE_ACCESS_TOKEN=...
SQUARE_APPLICATION_ID=...
SQUARE_LOCATION_ID=...
SQUARE_ENVIRONMENT=production
```

Use `sandbox` values together, or `production` values together.  
Do not mix sandbox nonce/app/location with production token/environment.

---

## 4) Django Settings Pattern

In `settings.py`, load via dotenv and expose:

```python
SQUARE_ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
SQUARE_APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID", "")
SQUARE_LOCATION_ID = os.getenv("SQUARE_LOCATION_ID", "")
SQUARE_ENVIRONMENT = os.getenv("SQUARE_ENVIRONMENT", "production").strip().lower()
```

---

## 5) Data Model Pattern

This project uses:

- `AIUserSubscription`:
  - `user` (OneToOne)
  - `plan` (`free`, `pro`, `one-year`)
  - `expiration_date`
- `SquareCustomer`:
  - `user` (ForeignKey)
  - `customer_id` (unique)
  - `card_id` (unique)

For reuse, keep at least:

- a subscription table with plan + expiration
- a Square customer mapping table with Square customer ID

---

## 6) URL Endpoints

From `myapp/urls.py`:

- `upgrade-to-pro/` -> payment page
- `process-ai-subscription/` -> backend charge endpoint

Admin renewal endpoints in `myapp/admin_urls.py`:

- `renewals/generate-links/`
- `renewals/send-links/`

---

## 7) Frontend Flow (Web Payments SDK)

In `upgrade_to_pro.html`, this project:

1. Loads Square SDK:
   - `https://web.squarecdn.com/v1/square.js`
2. Uses server-rendered env values:
   - `SQUARE_APPLICATION_ID`
   - `SQUARE_LOCATION_ID`
3. Creates card object:
   - `payments = Square.payments(appId, locationId)`
   - `card = await payments.card()`
4. Tokenizes card:
   - `result = await card.tokenize()`
5. Sends payload to backend:
   - `source_id` + selected plan + billing/contact fields

Important safeguards implemented:

- Blocks checkout on insecure context (non-HTTPS, except localhost).
- Blocks checkout when app/location IDs are missing.
- Shows user-friendly tokenization errors.

---

## 8) Backend Payment Flow (`process_ai_subscription`)

In `myapp/views.py`:

1. Parse JSON payload:
   - `source_id`, `plan`, `email`, billing fields.
2. Validate:
   - method must be POST
   - email required
   - plan must exist in `PLAN_PRICES`
3. Ensure user exists:
   - `User.objects.get_or_create(email=...)`
4. Ensure Square customer exists:
   - Search by email in Square
   - Create customer if not found
5. Create payment:
   - `square_client.payments.create_payment(...)`
   - includes `idempotency_key`, `amount_money`, `customer_id`, `buyer_email_address`
   - includes `billing_address` if available
6. Handle payment errors:
   - returns actionable message
   - special handling for decline codes (`GENERIC_DECLINE`, etc.)
7. Optional card save:
   - `square_client.cards.create_card(...)`
   - failures are logged but do not block successful checkout
8. Activate subscription:
   - set expiration based on plan
   - `AIUserSubscription.objects.update_or_create(...)`

Square client initialization pattern:

```python
square_client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment=settings.SQUARE_ENVIRONMENT,
)
```

---

## 9) Renewal Link Workflow (Reusable Pattern)

This project supports subscription renewals without manual payment coordination:

1. Admin selects due users.
2. Server creates signed token with:
   - `user_id`
   - `email`
   - `plan`
3. Tokenized URL points to `upgrade-to-pro` with `renewal_token`.
4. Page pre-fills email/plan and optionally greets by name.
5. User pays through same checkout path.

Security detail:

- Uses Django `signing.dumps` / `signing.loads` with `max_age` (30 days).

---

## 10) Common Issues and Fixes

### A) `INVALID_CARD_DATA` / nonce not found

Cause: App ID/location/environment mismatch between frontend and backend.  
Fix: Keep `SQUARE_APPLICATION_ID`, `SQUARE_LOCATION_ID`, `SQUARE_ACCESS_TOKEN`, and `SQUARE_ENVIRONMENT` from the same Square environment.

### B) `GENERIC_DECLINE`

Cause: Issuer/bank decline.  
Fix: Show clear message to user and allow retry/different card.

### C) SDK secure-context error

Cause: Square Web SDK requires HTTPS (or localhost).  
Fix: block UI and show guidance unless secure context.

### D) Duplicate/constraint issues on saved cards

Cause: forcing DB writes before valid card save.  
Fix: only persist `card_id` after successful `create_card`; make card-save non-blocking.

---

## 11) Reuse Checklist (Copy to New Project)

- [ ] Install `squareup`
- [ ] Add Square env vars in `.env`
- [ ] Expose vars in `settings.py`
- [ ] Add subscription model and Square customer model
- [ ] Add checkout page with Square SDK tokenization
- [ ] Add backend endpoint for processing subscription payment
- [ ] Add idempotency key and structured error handling
- [ ] Add secure-context checks in frontend
- [ ] Add renewal signed-link flow (optional but recommended)
- [ ] Test in sandbox fully before production

---

## 12) Minimal API Contract (Frontend -> Backend)

`POST /process-ai-subscription/` JSON payload:

```json
{
  "source_id": "cnon:card-nonce",
  "plan": "pro",
  "email": "user@example.com",
  "givenName": "Jane",
  "familyName": "Doe",
  "addressLine1": "175 S. 3rd St",
  "city": "Columbus",
  "state": "OH",
  "countryCode": "US",
  "phone": "+17405830770"
}
```

Success response:

```json
{ "success": true, "message": "Subscription activated!" }
```

Error response:

```json
{ "error": "Human-readable message" }
```

---

## 13) Suggested Improvements for Future Projects

- Add webhook handling (`payment.updated`) for async reconciliation.
- Save Square payment ID in a transaction model for audit trails.
- Add retry-safe renewal jobs with background workers.
- Add unit/integration tests for:
  - plan validation
  - decline mapping
  - renewal-token expiration

