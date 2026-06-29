# Odoo 19 Technical Module Validation

## Status of this repository

The manifests parse and use the best-known Odoo 19 technical names. This is a
static repository result, not proof that every name exists in a particular
Odoo Enterprise snapshot. Final confirmation must happen in the target
Odoo.sh build because Enterprise source is not public and integration modules
can move between releases.

## Confirmed in public Odoo 19 source

The following families are present in the public `odoo/odoo` 19.0 source and
are treated as stable:

| Area | Technical names |
|---|---|
| Base/collaboration | `base`, `base_setup`, `contacts`, `mail`, `calendar` |
| Commercial | `crm`, `sale_management`, `sale_crm`, `sale_stock`, `purchase`, `purchase_stock` |
| Finance/stock | `account`, `stock`, `stock_account`, `delivery`, `stock_landed_costs` |
| Warehouse | `stock_picking_batch`, `product_expiry` |
| Projects/people | `project`, `hr`, `hr_timesheet`, `hr_recruitment`, `hr_holidays`, `hr_attendance` |
| Website/marketing base | `website`, `website_sale`, `website_sale_stock`, `website_crm`, `website_livechat`, `payment`, `mass_mailing`, `sms`, `utm`, `link_tracker` |
| Manufacturing base | `mrp`, `mrp_account`, `mrp_subcontracting`, `purchase_mrp` where used by standard dependencies |

Reference:
[`odoo/odoo` 19.0 addons](https://github.com/odoo/odoo/tree/19.0/addons).

## Enterprise/build validation required

| Technical name | Used by | Why it must be checked |
|---|---|---|
| `web_studio` | 00, 01, 14, 15 | Enterprise-only Studio package |
| `stock_barcode` | 01, 04, 11 | Enterprise barcode UI |
| `industry_fsm` | 01, 08 | Field Service app |
| `industry_fsm_sale` | 01, 08 | Sales-to-FSM integration |
| `industry_fsm_stock` | 01, 08 | Products/stock in FSM |
| `helpdesk` | 01, 08 | Enterprise Helpdesk |
| `helpdesk_fsm` | 08 | Helpdesk-to-FSM integration |
| `documents` | 01, 07, 12, 14, 15, 16 | Enterprise Documents |
| `sign` | 01, 07, 14, 15 | Enterprise Sign |
| `approvals` | 01, 12, 14, 15 | Enterprise Approvals |
| `spreadsheet_dashboard` | 01, 11, 14, 15, 16 | Dashboard technical package |
| `appointment` | 02 | Appointments package |
| `marketing_automation` | 02, 13 | Enterprise automation |
| `planning` | 07, 08, 12 | Enterprise Planning |
| `mrp_workorder` | 10, 11 | Work Orders/Shop Floor package |
| `quality_control` | 10, 11 | Quality base package |
| `quality_mrp` | 10, 11 | MRP/Quality integration |
| `quality_stock` | 11 | Stock/Quality integration |
| `maintenance` | 10, 11 | Maintenance app/package in target build |
| `mrp_maintenance` | 10, 11 | MRP/Maintenance integration |
| `mrp_plm` | 11 | PLM |
| `mrp_subcontracting_purchase` | 11 | Purchase/subcontracting integration |
| `repair` | 08, 11 | Repairs technical package |
| `pos_loyalty` | 05 | POS loyalty integration |
| `pos_hr` | 05 | POS employee integration |
| `hr_appraisal` | 12 | Appraisals |
| `hr_skills` | 12 | Skills package/integration |
| `social` | 13 | Social Marketing |
| `account_reports` | 15 | Enterprise financial reports |
| `knowledge` | 15, 16 | Knowledge |
| `ai` | 16 | Odoo 19 AI application technical name |

These names remain hard dependencies because they define the requested branch
scenarios. If one is absent, do not guess a replacement. Search Apps in
developer mode, inspect the build source/addons list, record the actual name,
then change the manifest and this file together.

## Optional dependency rule

Move a module from `depends` to the branch's optional-app documentation only
when:

1. the target build proves it does not exist or is not licensed;
2. the meta module still delivers its stated core story;
3. the missing integration is covered by a documented manual configuration or
   intentionally omitted;
4. a clean build verifies installation.

## Odoo 19 compatibility decisions

- The base addon uses stable `res.partner.category` XML records under
  `noupdate="1"`.
- An unused demo-manager group was removed. Odoo 19's public `res.groups`
  model uses `privilege_id`; the older direct `category_id` field shape is not
  safe for a 19.0 data record.
- Odoo 19 product templates use `type="consu"` for goods and expose
  `is_storable` when Inventory is installed. Seeders introspect fields before
  setting `is_storable`.
- The seeders use `/xmlrpc/2`. Odoo 19 documentation marks legacy XML-RPC and
  JSON-RPC services as deprecated in favor of JSON-2. The scripts remain
  appropriate for this Odoo 19 demo lab, but a JSON-2 migration should be
  scheduled before the documented removal release.

References:

- [Odoo 19 product template source](https://github.com/odoo/odoo/blob/19.0/addons/product/models/product_template.py)
- [Odoo 19 `res.groups` source](https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/models/res_groups.py)
- [Odoo 19 External RPC API](https://www.odoo.com/documentation/19.0/developer/reference/external_rpc_api.html)
- [Odoo 19 External JSON-2 API](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)

## Validation worksheet

Copy one row per build and commit the result:

| Date | Branch | Odoo build/version | Meta module installed | Substitutions | Operator |
|---|---|---|---|---|---|
| _pending_ | `demo/01-al-noor-live-os` | _pending_ | No | None recorded | _pending_ |

Do not change `_pending_` until a clean Odoo.sh installation has actually
completed.
