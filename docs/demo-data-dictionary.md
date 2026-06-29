# Demo Data Dictionary

Seeder-owned records use the external-ID module `mindora_demo_seed`. Values are
fictional and must remain free of real customer information.

## Partners

| Scenario | Record | Key | External ID |
|---|---|---|---|
| Al Noor | Gulf Towers Facilities LLC | `facilities@gulftowers.demo` | `mindora_demo_seed.al_noor_customer_gulf_towers` |
| Al Noor | Muscat Smart Properties | `info@muscatsmart.demo` | `mindora_demo_seed.al_noor_customer_muscat_smart` |
| Al Noor | Oman Industrial Services | `ops@omanindustrial.demo` | `mindora_demo_seed.al_noor_customer_oman_industrial` |
| Al Noor | Delta Security Supplies | `sales@deltasecurity.demo` | `mindora_demo_seed.al_noor_vendor_delta_security` |
| Al Noor | Gulf Network Hardware | `sales@gulfnetwork.demo` | `mindora_demo_seed.al_noor_vendor_gulf_network` |
| Services | Bank Muscat Digital | `digital@bankmuscat.demo` | `mindora_demo_seed.services_customer_01` |
| Services | Oman Air eCommerce | `ecommerce@omanair.demo` | `mindora_demo_seed.services_customer_02` |
| Services | Renaissance Services | `digital@renaissance.demo` | `mindora_demo_seed.services_customer_03` |
| Holding | Clarence Holding | `holding@clarence.demo` | `mindora_demo_seed.holding_company_01` |
| Holding | Clarence Industrial | `industrial@clarence.demo` | `mindora_demo_seed.holding_company_02` |
| Holding | Clarence Digital | `digital@clarence.demo` | `mindora_demo_seed.holding_company_03` |
| Holding | Clarence Properties | `properties@clarence.demo` | `mindora_demo_seed.holding_company_04` |

Holding “companies” are partner records by default. With the explicit
`--create-companies` flag, the seeder also creates
`mindora_demo_seed.holding_res_company_01` … `_04`; accounting setup remains
manual.

## Users and personas

Users are configured manually so passwords, groups, and mail behavior are never
seeded into source code.

| Persona | Role | Required access |
|---|---|---|
| Fatma | Salesperson | CRM/Sales user |
| Khalid | Sales approver | Sales manager and approval authority |
| Salim | Field technician | Field Service, timesheets, limited stock |
| Maryam | Buyer/warehouse | Purchase and Inventory |
| Aisha | Accountant | Billing/Accounting |
| Sultan | Managing director | Read/reporting access |

Use `.demo` logins and never real employee addresses.

## Products

| Internal reference | Name | Type | External ID |
|---|---|---|---|
| `ANS-ACC-CTRL` | Access Control Controller | Goods/storable | `mindora_demo_seed.al_noor_product_access_controller` |
| `ANS-DOOR-RDR` | Smart Door Reader | Goods/storable | `mindora_demo_seed.al_noor_product_door_reader` |
| `ANS-NET-CAB` | Network Cabinet | Goods/storable | `mindora_demo_seed.al_noor_product_network_cabinet` |
| `RM-SHEET` | Galvanised Steel Sheet 1.2 mm | Goods/storable | `mindora_demo_seed.mrp_product_rm_sheet` |
| `RM-ANGLE` | Steel Angle Profile | Goods/storable | `mindora_demo_seed.mrp_product_rm_angle` |
| `RM-FAST` | Fastener & Bracket Set | Goods/storable | `mindora_demo_seed.mrp_product_rm_fast` |
| `RM-COAT` | Powder Coat | Goods/storable | `mindora_demo_seed.mrp_product_rm_coat` |
| `FG-AHU-FRAME` | Rooftop AHU Steel Frame | Goods/storable | `mindora_demo_seed.mrp_product_finished_ahu_frame` |

## Services

| Internal reference | Name | External ID |
|---|---|---|
| `ANS-SVC-INST` | Installation Service | `mindora_demo_seed.al_noor_service_installation` |
| `ANS-SVC-PMP` | Preventive Maintenance Plan | `mindora_demo_seed.al_noor_service_maintenance` |
| `ANS-SVC-ESV` | Emergency Site Visit | `mindora_demo_seed.al_noor_service_emergency_visit` |
| `SV-CONSULT` | Consulting Day Rate | `mindora_demo_seed.services_product_consulting` |
| `SV-IMPL` | Software Implementation (Fixed) | `mindora_demo_seed.services_product_implementation` |
| `SV-SUPPORT` | Managed Support (Monthly) | `mindora_demo_seed.services_product_support` |

## Opportunities

| Scenario | Name | External ID |
|---|---|---|
| Al Noor | Gulf Towers — Access Control Upgrade | `mindora_demo_seed.al_noor_opportunity_gulf_towers` |
| Holding | New Logistics Park — Feasibility | `mindora_demo_seed.holding_opportunity_logistics_park` |

## Sales orders

| Scenario | Record | Start state | External ID |
|---|---|---|---|
| Al Noor | Gulf Towers anchor quotation | Draft; origin `MINDORA-DEMO-ANCHOR` | `mindora_demo_seed.al_noor_anchor_quotation` |

The operator may duplicate the anchor quotation for rehearsals. Transactional
copies are not assigned stable external IDs.

## Projects and tasks

| Scenario | Record | External ID/pattern |
|---|---|---|
| Al Noor | Field Service project | `mindora_demo_seed.al_noor_fsm_project` when the seeder creates it |
| Al Noor | Gulf Towers — Access Control Site Visit | `mindora_demo_seed.al_noor_fsm_task` |
| Services | Bank Muscat — Mobile App | `mindora_demo_seed.services_project_bank_muscat_mobile` |
| Services | Discovery, UX design, API build, App build, UAT, Go-live | `mindora_demo_seed.services_task_01` … `_06` |
| Holding | `[HLD-001] Group Platform Build` | `mindora_demo_seed.holding_project_01` |
| Holding | `[HLD-002] Plant Expansion Phase 2` | `mindora_demo_seed.holding_project_02` |
| Holding | `[HLD-003] Logistics Park Development` | `mindora_demo_seed.holding_project_03` |

## Documents and governance

| Scenario | Record | External ID |
|---|---|---|
| Al Noor | Site Works Approval | `mindora_demo_seed.al_noor_approval_site_works` |
| Al Noor | Gulf Towers — Site Scope and Drawings placeholder | `mindora_demo_seed.al_noor_document_scope_placeholder` |
| Holding | Capital Expenditure / Investment | `mindora_demo_seed.holding_approval_capex` |
| Holding | Board Pack — Current Quarter placeholder | `mindora_demo_seed.holding_document_01` |
| Holding | Investment Committee — Pipeline placeholder | `mindora_demo_seed.holding_document_02` |

URL attachments point to `example.invalid` by design. Replace them in the demo
database with sanitized files; do not commit customer documents.

## Field Service

| Record | Configuration owner | Notes |
|---|---|---|
| Gulf Towers site visit | Seeder + operator | Seeder creates task; operator assigns technician/date/worksheet |
| Worksheet template | Operator | Enterprise schema and Studio fields are build-sensitive |
| Products used | Rehearsal transaction | Reset stock or restore baseline |
| Customer signature/photo | Optional operator setup | Use sanitized content only |

## Manufacturing records

| Record | External ID |
|---|---|
| Cutting work centre | `mindora_demo_seed.mrp_workcenter_01` |
| Welding work centre | `mindora_demo_seed.mrp_workcenter_02` |
| Finishing / Powder Coat work centre | `mindora_demo_seed.mrp_workcenter_03` |
| Quality / QC work centre | `mindora_demo_seed.mrp_workcenter_04` |
| Rooftop AHU Steel Frame BoM | `mindora_demo_seed.mrp_bom_finished_ahu_frame` |
| Draft manufacturing order | `mindora_demo_seed.mrp_production_demo` |

The quality point remains a manual target-build step because required
Enterprise fields can vary. Record its exact setup in the build validation
worksheet.
