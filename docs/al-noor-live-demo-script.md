# Al Noor Live Demo Script

## Positioning

**Company:** Al Noor Integrated Solutions

**Audience:** owner, operations lead, finance lead, and functional managers

**Core line:** “Odoo provides the platform. Mindora designs the business
operating system.”

The demo proves one connected operating path. It is not an app tour.

## Hero records and start state

| Record | Required start state |
|---|---|
| Customer | `Gulf Towers Facilities LLC` |
| Opportunity | `Gulf Towers — Access Control Upgrade`, Qualification stage |
| Equipment | `Access Control Controller`, `Smart Door Reader`, `Network Cabinet` |
| Services | `Installation Service`, `Preventive Maintenance Plan`, `Emergency Site Visit` |
| Vendor | `Delta Security Supplies` or `Gulf Network Hardware` |
| Quotation | Draft, Gulf Towers, at least one equipment and one service line |
| Field task | `Gulf Towers — Access Control Site Visit`, assigned and scheduled |
| Approval | Confirm button approval step or `Site Works Approval` request ready |
| Dashboard | Populated Al Noor management dashboard |

The seeder prepares lightweight master and anchor records. Finish approval,
worksheet, dashboard, stock, and user assignment manually.

## Opening narration

“Al Noor sells equipment, installs it, and maintains it. The management problem
is not a missing CRM or accounting screen. It is the handoff between teams.
We will follow one customer requirement from the first conversation to
delivery, site work, invoicing, and management visibility.”

## 7-minute executive version

### 0:00–0:45 — Lead to opportunity

Click:

1. Open **CRM**.
2. Open `Gulf Towers — Access Control Upgrade`.
3. Show customer, expected revenue, salesperson, next activity, and chatter.
4. Move it to the next stage only if that move is part of the rehearsed reset.

Say: “The commercial record is also the coordination point: owner, activity,
history, and customer context stay together.”

Do not click: CRM configuration, stage editor, lead import, or developer tools.

### 0:45–1:45 — Quotation and approval

Click:

1. Click **New Quotation** from the opportunity, or open the prepared draft.
2. Show `Access Control Controller`, `Smart Door Reader`, and
   `Installation Service`.
3. Click the approval avatar beside **Confirm**.
4. Approve from the pre-authenticated approver session, then return and confirm.

Say: “Mindora places control at the decision point. The approver gets an
activity, the decision is recorded in chatter, and the salesperson stays in
the process.”

Fallback if Studio approval is not configured: open the prepared
`Site Works Approval` request, approve it, then return to the quotation.

Do not click: Studio rule editor, access-rights screens, taxes, or quotation
template configuration.

### 1:45–2:45 — Fulfillment and procurement

Click:

1. On the confirmed order, open the **Delivery** smart button.
2. Show reserved versus unavailable equipment.
3. Open **Inventory → Operations → Replenishment**.
4. Open the prepared draft request/PO to the vendor.

Say: “The sale creates operational demand. Stock and purchasing see the same
requirement without rekeying.”

Do not click: routes, push/pull rules, valuation layers, or scheduler internals.

### 2:45–4:30 — Field Service

Click:

1. Return to the sales order and open the **Tasks** smart button.
2. Open `Gulf Towers — Access Control Site Visit`.
3. Show customer, address, assignee, scheduled date, worksheet, timesheet, and
   products.
4. Add one rehearsed part, complete the worksheet, and mark the task done.

Say: “The technician sees the job, customer, checklist, time, and parts in one
mobile-ready task. Products used update the commercial and stock trail.”

Do not click: worksheet designer, project settings, mobile login, or a map that
has not been preloaded.

### 4:30–5:30 — Invoice

Click:

1. From the order/task flow, click **Create Invoice**.
2. Open the prepared draft invoice; post only if the journal and taxes were
   rehearsed.
3. Open Gulf Towers and show the related documents/smart buttons.

Say: “Finance receives billable evidence from the same execution record. The
invoice is the financial continuation of the work, not a detached re-entry.”

Do not click: chart of accounts, tax setup, payment provider, or journal entry
debug screens.

### 5:30–7:00 — Dashboard and close

Click:

1. Open the prepared Al Noor dashboard.
2. Show revenue, open orders, overdue receivables, replenishment exceptions,
   and open field jobs.
3. Drill from one tile to the underlying records.

Say: “Management gets one operating view because the underlying process is
connected. Odoo is the platform. Mindora designed the operating system around
how Al Noor actually sells, fulfills, services, and controls.”

## 20-minute standard version

Use the 7-minute path and add the following controlled details.

### CRM and activity discipline — 3 minutes

1. Open the opportunity.
2. Show source/campaign only if populated.
3. Open the next activity and reschedule it once.
4. Show the chatter entry.
5. Create/open the quotation.

Explain ownership, activity discipline, and the elimination of side-channel
follow-up lists.

### Quote, margin, and approval — 3 minutes

1. Review quantities and price.
2. Apply the rehearsed discount that activates the approval condition.
3. Click the approver avatar.
4. Switch to the approver session; approve.
5. Return, show chatter, confirm.

Explain that Studio approval rules bind control to the button action. Use a
native Approvals request only as the prepared fallback.

### Stock and purchase handoff — 3 minutes

1. Open delivery from the order.
2. Show availability by product.
3. Open replenishment for one short item.
4. Open the proposed purchase order and vendor.
5. Return without confirming/receiving unless reset has been rehearsed.

Explain demand visibility, vendor linkage, and warehouse ownership.

### Field execution — 4 minutes

1. Open the generated task.
2. Show schedule and technician.
3. Start timer.
4. Complete the three-item worksheet.
5. Add one product used.
6. Stop timer and mark done.
7. Return to the back office and show status.

Explain technician usability, evidence, parts consumption, and billable
handoff.

### Finance and management — 4 minutes

1. Open/create invoice.
2. Show posted versus overdue status using prepared records.
3. Open dashboard.
4. Drill into overdue invoices.
5. Return to dashboard and close.

Explain that KPIs retain record-level traceability.

### Questions buffer — 3 minutes

Answer from the existing screen. Do not open unrehearsed configuration. Park
deep technical questions for a post-demo architecture session.

## 45-minute workshop version

Use this agenda:

| Time | Segment | Outcome |
|---:|---|---|
| 0–5 | Business framing | Align on Al Noor's operating problem |
| 5–12 | CRM and activity | Show ownership and customer context |
| 12–20 | Quotation and control | Demonstrate pricing and approval evidence |
| 20–27 | Stock and purchasing | Show demand-driven fulfillment |
| 27–35 | Field Service | Execute worksheet, time, parts, and completion |
| 35–40 | Finance | Show invoice and receivables |
| 40–44 | Dashboard | Drill from KPI to record |
| 44–45 | Close | Restate platform versus operating-system design |

For the workshop, allow one audience-selected branch:

- **Commercial:** sales stages, activities, quotation, approval.
- **Operations:** availability, replenishment, delivery, field task.
- **Control:** invoice, overdue follow-up, dashboard drill-down.

Do not attempt all three branches in depth.

## Approval setup

Preferred Odoo 19 setup:

1. Open the prepared quotation and start **Studio**.
2. Select **Confirm**.
3. Add an approval step.
4. Set the sales manager/approver group.
5. Add a condition for the rehearsed threshold, such as total above the agreed
   amount or the explicit demo flag.
6. Add a short description.
7. Test unauthorized click, activity creation, approval, chatter entry, and
   final confirmation.

Do not improvise a computed discount condition on demo day. If the condition
cannot be made deterministic, use a simple total threshold or the native
Approvals fallback.

## Field Service setup

1. Configure `Preventive Maintenance Plan` or `Emergency Site Visit` as a
   service that creates a task in the Field Service project.
2. Confirm a test order and verify the task smart button.
3. Assign a technician and scheduled date.
4. Set a default warehouse for the technician.
5. Add a worksheet with:
   - site access confirmed;
   - controller installed/tested;
   - reader alignment checked;
   - customer notes;
   - signature/photo only if stable.
6. Verify products used appear in the expected invoice/stock path.

## What not to click live

- Apps installation or module upgrades.
- Studio editor after the demo begins.
- Accounting localization, taxes, or journals.
- Inventory route configuration.
- Empty reports or dashboards.
- Real email recipients, payment providers, shipping connectors, or AI tools
  with write access.
- Any record containing unsanitized customer data.
- Browser developer tools or Odoo developer menus.

## Fallback plan

Prepare these assets after the final rehearsal:

| Failure | Fallback |
|---|---|
| CRM screen slow | Pipeline and opportunity screenshot |
| Approval not triggered | Approved native Approvals request screenshot |
| Replenishment missing | Delivery plus prepared draft PO screenshot |
| Mobile/worksheet failure | 60–90 second recorded technician flow |
| Invoice posting blocked | Prepared posted invoice screenshot |
| Dashboard slow/empty | Exported populated dashboard image |
| Database unavailable | Narrated sequence using all fallback assets |

If a screen does not respond within eight seconds, stop clicking and move to
the fallback. Never debug during the presentation.

## Pre-flight

- Run the full path once at least 60 minutes before the session.
- Reset mutable records using `demo-reset-runbook.md`.
- Pre-authenticate salesperson, approver, technician, and manager sessions.
- Confirm Odoo.sh mail catcher and no real outbound recipients.
- Turn developer mode and notifications off.
- Keep fallback assets local to the presentation machine.
- Confirm the final dashboard drill-down lands on a populated record.
