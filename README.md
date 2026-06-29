# Mindora × Clarence Odoo 19 Demo Lab

This repository is the working GitHub/Odoo.sh home for the Clarence / Mindora Odoo 19 Enterprise demo environments.

## Positioning

> Odoo provides the platform. Mindora designs the business operating system.

The repository is organised around demo branches. Each branch should become a separate Odoo.sh database for a different business operating model.

## Demo branch map

| Branch | Purpose | Odoo.sh database |
|---|---|---|
| `demo/00-base-universal` | Universal clean baseline | `mindora-demo-00-base` |
| `demo/01-al-noor-live-os` | Main live demo: Al Noor operating system | `mindora-demo-01-al-noor` |
| `demo/02-sales` | CRM / sales engine | `mindora-demo-02-sales` |
| `demo/03-trading-distribution-basic` | Basic trading and distribution | `mindora-demo-03-trading-basic` |
| `demo/04-trading-distribution-warehouse` | Warehouse, barcode, replenishment | `mindora-demo-04-warehouse` |
| `demo/05-retail-pos` | Retail / POS / showroom | `mindora-demo-05-pos` |
| `demo/06-ecommerce-omnichannel` | Website + eCommerce + inventory | `mindora-demo-06-ecommerce` |
| `demo/07-project-services` | Project services and timesheets | `mindora-demo-07-project-services` |
| `demo/08-field-service-after-sales` | Field service and after-sales | `mindora-demo-08-field-service` |
| `demo/09-workshop-manufacturing-l1` | Small workshop manufacturing | `mindora-demo-09-workshop` |
| `demo/10-manufacturing-l2` | Factory production control | `mindora-demo-10-manufacturing-l2` |
| `demo/11-production-l3` | Advanced production / PLM / quality | `mindora-demo-11-production-l3` |
| `demo/12-hr` | HR and people operations | `mindora-demo-12-hr` |
| `demo/13-marketing` | Marketing and growth engine | `mindora-demo-13-marketing` |
| `demo/14-governance` | Documents, approvals, sign, control | `mindora-demo-14-governance` |
| `demo/15-holding` | Clarence-style holding control tower | `mindora-demo-15-holding` |
| `demo/16-ai-control-room` | AI agent / executive control room | `mindora-demo-16-ai` |

## Build priority

Build these first:

1. `demo/00-base-universal`
2. `demo/01-al-noor-live-os`
3. `demo/04-trading-distribution-warehouse`
4. `demo/08-field-service-after-sales`
5. `demo/10-manufacturing-l2`
6. `demo/15-holding`

The rest are specialist proof environments.

## Important rule

Do not demonstrate Odoo as an app list. Demonstrate it as connected operating flow:

```text
Apps → Processes → Ecosystems → Operating System
```

## First live demo

Use `demo/01-al-noor-live-os` as the anchor live demo. It should show:

1. CRM lead / opportunity
2. Quotation and sales order
3. Inventory / purchase / delivery
4. Field service / task / worksheet / products
5. Documents / approvals / sign
6. Dashboard / control layer

## Safety

Never run seeders against production. Use Odoo.sh demo/staging databases only.
