# Branch Installation Guide

Install one branch meta module per database. Standard Odoo applications listed
as **required** are installed through the meta module dependencies. Items under
**optional** are deliberate operator choices and must not silently become hard
dependencies.

## 00 — Base Universal

- **Branch:** `demo/00-base-universal`
- **Database:** `mindora-demo-00-base`
- **Meta module:** `mindora_demo_00_base_universal`
- **Purpose:** reusable cross-functional baseline.
- **Required apps:** Contacts, Calendar, CRM, Sales, Accounting, Purchase,
  Inventory, Project, Employees, Timesheets, Studio.
- **Optional apps:** Documents, Sign, Approvals.
- **Post-install:** enable leads if the database will demonstrate lead
  qualification; set company, currency, timezone, and demo users.
- **Seeder:** none.
- **Story:** show that a single operating baseline connects customer,
  commercial, fulfillment, finance, and people records.

## 01 — Al Noor Live OS

- **Branch:** `demo/01-al-noor-live-os`
- **Database:** `mindora-demo-01-al-noor`
- **Meta module:** `mindora_demo_01_al_noor_live_os`
- **Purpose:** flagship B2B trading, installation, and maintenance demo.
- **Required apps:** CRM, Sales, Purchase, Inventory, Barcode, Accounting,
  Project, Timesheets, Field Service, Helpdesk, Documents, Sign, Approvals,
  Spreadsheet Dashboards, Studio.
- **Optional apps:** Planning, Repairs, Knowledge.
- **Post-install:** enable leads; configure the maintenance service to create
  Field Service tasks; assign a default field warehouse; create the worksheet,
  approval step, and management dashboard.
- **Seeder:** `scripts/seeders/seed_al_noor.py`.
- **Story:** Lead → Opportunity → Quotation → Sales Order → Delivery/Purchase →
  Field Service → Invoice → Dashboard.

## 02 — Sales

- **Branch:** `demo/02-sales`
- **Database:** `mindora-demo-02-sales`
- **Meta module:** `mindora_demo_02_sales`
- **Purpose:** CRM and sales engine.
- **Required apps:** CRM, Sales, CRM/Sales integration, Email Marketing,
  Marketing Automation, Website CRM, Appointments.
- **Optional apps:** Live Chat, SMS Marketing, Sign.
- **Post-install:** enable leads; configure stages, activity plans, sales teams,
  website lead form, appointment resource, and one mailing audience.
- **Seeder:** none; reuse safe native demo contacts and add two named
  opportunities manually.
- **Story:** inbound lead → qualification activity → appointment → quotation →
  campaign attribution.

## 03 — Commerce

- **Branch:** `demo/03-commerce`
- **Database:** `mindora-demo-03-commerce`
- **Meta module:** `mindora_demo_03_commerce`
- **Purpose:** basic trading and distribution.
- **Required apps:** Sales, Purchase, Inventory, Accounting, Delivery, Landed
  Costs.
- **Optional apps:** Barcode, Quality.
- **Post-install:** configure one vendor, route, warehouse, delivery method,
  payment term, and landed-cost service product.
- **Seeder:** none.
- **Story:** customer demand → procurement → receipt → landed cost → delivery →
  margin.

## 04 — Core Warehouse

- **Branch:** `demo/04-core`
- **Database:** `mindora-demo-04-core`
- **Meta module:** `mindora_demo_04_core`
- **Purpose:** warehouse, barcode, replenishment, and stock discipline.
- **Required apps:** Sales, Purchase, Inventory, Barcode, Batch Transfers,
  Delivery, Landed Costs, Expiration Dates.
- **Optional apps:** Quality, IoT.
- **Post-install:** enable storage locations, multi-step routes, lots/serials,
  expiration dates, packages, and GS1 only when the scanner sheet uses it.
- **Seeder:** none.
- **Story:** scan receipt → putaway → replenish → batch pick → delivery with
  traceability.

## 05 — Retail

- **Branch:** `demo/05-retail`
- **Database:** `mindora-demo-05-retail`
- **Meta module:** `mindora_demo_05_retail`
- **Purpose:** retail, POS, and showroom.
- **Required apps:** Point of Sale (including its Odoo 19 stock/accounting
  integration), POS/Sales, Loyalty, POS Employees, Sales.
- **Optional apps:** eCommerce, Barcode, Gift Cards if exposed by the build.
- **Post-install:** create one POS configuration, payment methods, cashier,
  loyalty program, opening cash, and showroom stock.
- **Seeder:** none.
- **Story:** identify customer → sell → redeem loyalty → update stock →
  reconcile session.

## 06 — Online

- **Branch:** `demo/06-online`
- **Database:** `mindora-demo-06-online`
- **Meta module:** `mindora_demo_06_online`
- **Purpose:** website, eCommerce, and inventory.
- **Required apps:** Website, eCommerce, stock availability, Website CRM, Live
  Chat, Payments, Delivery, Sales, Inventory, Accounting, Email Marketing.
- **Optional apps:** Coupons, Product Comparison, Helpdesk.
- **Post-install:** publish three sanitized products; configure B2B checkout
  fields, test payment provider, delivery method, contact form, and portal.
- **Seeder:** none.
- **Story:** website visit → B2B enquiry/order → payment/delivery → fulfillment
  → portal.

## 07 — Client Work

- **Branch:** `demo/07-client-work`
- **Database:** `mindora-demo-07-client-work`
- **Meta module:** `mindora_demo_07_client_work`
- **Purpose:** project services, timesheets, and profitability.
- **Required apps:** Project, Timesheets, Sales, Sales/Project,
  Sales/Timesheets, Accounting, Planning, Documents, Sign.
- **Optional apps:** Subscriptions, Helpdesk, Knowledge; validate the Odoo 19
  technical module before adding it as a dependency.
- **Post-install:** set employee costs, billable service product, project
  stages, planning roles, analytic account, and profitability permissions.
- **Seeder:** `scripts/seeders/seed_services.py`.
- **Story:** Meridian Digital sells a project and recurring support → plan team
  → record time → invoice → inspect project margin.

## 08 — Field Service and After-Sales

- **Branch:** `demo/08-field-service-after-sales`
- **Database:** `mindora-demo-08-field-service`
- **Meta module:** `mindora_demo_08_field_service_after_sales`
- **Purpose:** field service, helpdesk, repairs, worksheets, and parts.
- **Required apps:** Field Service and Sales/Stock integrations, Sales,
  Projects, Timesheets, Inventory, Accounting, Helpdesk, Helpdesk/FSM,
  Repairs, Planning.
- **Optional apps:** Sign, Documents, Barcode.
- **Post-install:** configure helpdesk-to-task action, service tracking,
  worksheet, default technician warehouse, time/material invoicing, and repair
  operation type.
- **Seeder:** `scripts/seeders/seed_al_noor.py`.
- **Story:** support ticket/order → scheduled technician → worksheet and parts
  → repair/invoice → service history.

## 09 — Workshop

- **Branch:** `demo/09-workshop`
- **Database:** `mindora-demo-09-workshop`
- **Meta module:** `mindora_demo_09_workshop`
- **Purpose:** small workshop manufacturing.
- **Required apps:** Manufacturing, Inventory, Stock Accounting, Purchase,
  Sales, Accounting.
- **Optional apps:** Barcode, Maintenance.
- **Post-install:** configure one warehouse, manufacturing route, units, simple
  BoM, component stock, and replenishment.
- **Seeder:** `scripts/seeders/seed_mrp.py`.
- **Story:** quotation/demand → components → manufacturing order → finished
  receipt → delivery.

## 10 — MRP

- **Branch:** `demo/10-mrp`
- **Database:** `mindora-demo-10-mrp`
- **Meta module:** `mindora_demo_10_mrp`
- **Purpose:** factory manufacturing level 2.
- **Required apps:** Manufacturing, Work Orders, MRP Accounting, Inventory,
  Purchase, Sales, Quality, Maintenance, Accounting.
- **Optional apps:** Barcode, Planning.
- **Post-install:** configure work centres, operations, quality point,
  equipment, maintenance team, and valuation.
- **Seeder:** `scripts/seeders/seed_mrp.py`.
- **Story:** Gulf Precision builds a Rooftop AHU Steel Frame → planned MO →
  work orders → quality → cost → maintenance insight.

## 11 — MRP Plus

- **Branch:** `demo/11-mrp-plus`
- **Database:** `mindora-demo-11-mrp-plus`
- **Meta module:** `mindora_demo_11_mrp_plus`
- **Purpose:** advanced manufacturing level 3.
- **Required apps:** MRP/Work Orders/Accounting, PLM, Subcontracting,
  Purchasing, Inventory, Barcode, Quality, Maintenance, Repairs, Dashboards.
- **Optional apps:** Documents, Sign.
- **Post-install:** validate PLM and subcontracting technical modules; configure
  engineering change stages, subcontractor route, serial traceability, and
  advanced quality checks.
- **Seeder:** `scripts/seeders/seed_mrp.py`; finish advanced records manually.
- **Story:** engineering change → subcontracted operation → traceable build →
  quality issue → repair/dashboard.

## 12 — Team

- **Branch:** `demo/12-team`
- **Database:** `mindora-demo-12-team`
- **Meta module:** `mindora_demo_12_team`
- **Purpose:** HR and people operations.
- **Required apps:** Employees, Recruitment, Time Off, Attendance, Appraisals,
  Skills, Planning, Projects, Timesheets, Approvals, Documents.
- **Optional apps:** Referrals, Fleet, Payroll only when localization is ready.
- **Post-install:** create departments, managers, appraisal template, goals,
  360 feedback, skills, shifts, and leave approvers.
- **Seeder:** none; extend native demo employees instead of duplicating them.
- **Story:** candidate → employee → skills/planning → goal and 360 appraisal →
  people analysis.

## 13 — Marketing

- **Branch:** `demo/13-marketing`
- **Database:** `mindora-demo-13-marketing`
- **Meta module:** `mindora_demo_13_marketing`
- **Purpose:** marketing and growth engine.
- **Required apps:** CRM, Sales, Website, Website CRM, Live Chat, Email
  Marketing, Marketing Automation, Social Marketing, SMS, UTM, Link Tracker.
- **Optional apps:** Events, Surveys.
- **Post-install:** configure sanitized mailing lists, one automation,
  campaign/UTM links, social sandbox, and metrics with no real recipients.
- **Seeder:** none.
- **Story:** campaign → landing form → lead → nurture → opportunity → delivered,
  opened, clicked, replied, and bounced metrics.

## 14 — Board

- **Branch:** `demo/14-board`
- **Database:** `mindora-demo-14-board`
- **Meta module:** `mindora_demo_14_board`
- **Purpose:** governance, documents, approvals, and signatures.
- **Required apps:** Documents, Sign, Approvals, Project, Accounting, Purchase,
  Sales, CRM, Studio, Mail, Dashboards.
- **Optional apps:** Knowledge.
- **Post-install:** create board workspace, document tags, approval categories,
  signature template, Studio approval step, and read-only dashboard.
- **Seeder:** `scripts/seeders/seed_holding.py`.
- **Story:** decision paper → approval → signature → action project → financial
  control.

## 15 — Holding

- **Branch:** `demo/15-holding`
- **Database:** `mindora-demo-15-holding`
- **Meta module:** `mindora_demo_15_holding`
- **Purpose:** Clarence-style holding control tower.
- **Required apps:** Accounting/Reports, Project, Employees, Timesheets,
  Documents, Sign, Approvals, CRM, Sales, Purchase, Inventory, Dashboards,
  Studio, Knowledge.
- **Optional apps:** Consolidation or localization-specific reporting only
  after technical-name validation.
- **Post-install:** configure permitted companies, intercompany access,
  initiative codes, board workspace, CapEx approval, knowledge sources, and
  executive dashboard. Do not create legal entities casually.
- **Seeder:** `scripts/seeders/seed_holding.py` creates portfolio contacts and
  initiatives. Add `--create-companies` only on the dedicated holding database
  to create the parent and three subsidiaries.
- **Story:** portfolio opportunity → initiative → document/CapEx approval →
  project and finance drill-down.

## 16 — Control Room

- **Branch:** `demo/16-room`
- **Database:** `mindora-demo-16-room`
- **Meta module:** `mindora_demo_16_room`
- **Purpose:** AI-enabled executive control room.
- **Required apps:** AI, Knowledge, Documents, CRM, Project, Accounting,
  Spreadsheet Dashboards.
- **Optional apps:** Helpdesk and any app-specific AI topic used in the room.
- **Post-install:** create a narrowly scoped agent, topics, tools, system prompt,
  and sanitized sources; restrict to sources where appropriate; test every
  action with least privilege.
- **Seeder:** none.
- **Story:** executive question → grounded source retrieval → operational view →
  human-approved follow-up.
