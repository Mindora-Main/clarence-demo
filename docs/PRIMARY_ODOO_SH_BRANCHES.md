# Primary Odoo.sh Branches

These short names are the supported Odoo.sh targets. Older verbose branches
may remain in Git history, but new build automation and documentation must use
this list.

| Build order | Branch | Meta module | Scenario |
|---:|---|---|---|
| 1 | `demo/01-al-noor-live-os` | `mindora_demo_01_al_noor_live_os` | Anchor live operating-system demo |
| 2 | `demo/00-base-universal` | `mindora_demo_00_base_universal` | Reusable cross-functional baseline |
| 3 | `demo/02-sales` | `mindora_demo_02_sales` | CRM and sales |
| 4 | `demo/03-commerce` | `mindora_demo_03_commerce` | Trading and distribution |
| 5 | `demo/04-core` | `mindora_demo_04_core` | Warehouse and barcode |
| 6 | `demo/05-retail` | `mindora_demo_05_retail` | Retail and POS |
| 7 | `demo/06-online` | `mindora_demo_06_online` | Website and eCommerce |
| 8 | `demo/07-client-work` | `mindora_demo_07_client_work` | Projects and timesheets |
| 9 | `demo/08-field-service-after-sales` | `mindora_demo_08_field_service_after_sales` | Field service and after-sales |
| 10 | `demo/09-workshop` | `mindora_demo_09_workshop` | Workshop manufacturing |
| 11 | `demo/10-mrp` | `mindora_demo_10_mrp` | Factory manufacturing |
| 12 | `demo/11-mrp-plus` | `mindora_demo_11_mrp_plus` | Advanced manufacturing |
| 13 | `demo/12-team` | `mindora_demo_12_team` | People operations |
| 14 | `demo/13-marketing` | `mindora_demo_13_marketing` | Marketing and growth |
| 15 | `demo/14-board` | `mindora_demo_14_board` | Board governance |
| 16 | `demo/15-holding` | `mindora_demo_15_holding` | Holding control tower |
| 17 | `demo/16-room` | `mindora_demo_16_room` | AI executive control room |

## Branch invariant

Each primary branch must point to the approved demo-lab baseline commit before
branch-specific changes are added. A branch database installs only its matching
meta module. Do not install all 17 meta modules into one database.

After the baseline commit is on `main`, create a missing branch with:

```bash
git switch main
git pull --ff-only origin main
git switch -c demo/NN-name
git push -u origin demo/NN-name
```

To fast-forward an existing branch that has no intentional divergence:

```bash
git switch demo/NN-name
git merge --ff-only main
git push origin demo/NN-name
```

Never force-update a branch that has independent demo configuration commits.
Merge or rebase it deliberately after reviewing its diff.
