# Ingest report

Written by `uv run p2 ingest`.
It lists every document in this corpus that ingest added, with what the cleaning pass did and anything that looks wrong.
Running ingest again adds to the table and replaces the "last run" section, and `uv run p2 ingest --report` rewrites it for the documents in docs/ now, after you removed some.

## Summary

- Documents: 406 (the final check needs at least 200)
- Words: 551,643
- Estimated tokens (words times 1.4): 772,300 (`p2 check` warns above 800,000 and fails above 1,000,000)
- Flagged documents: 0

## Documents

| docid | words | characters per page | flags | cleaning |
|---|---:|---:|---|---|
| `cbp-admission-forms-i94` | 599 | - | - | not added by p2 ingest |
| `cbp-applying-for-admission` | 1,878 | - | - | not added by p2 ingest |
| `cfr22-41.102` | 579 | - | - | not added by p2 ingest |
| `cfr22-41.121` | 720 | - | - | not added by p2 ingest |
| `cfr22-41.61` | 703 | - | - | not added by p2 ingest |
| `cfr22-41.62` | 705 | - | - | not added by p2 ingest |
| `cfr22-62.23-p01-purpose-through-the-student` | 1,299 | - | - | not added by p2 ingest |
| `cfr22-62.23-p02-student-employment-through-stu` | 2,025 | - | - | not added by p2 ingest |
| `cfr26-1.871-2` | 452 | - | - | not added by p2 ingest |
| `cfr26-1.871-9` | 503 | - | - | not added by p2 ingest |
| `cfr26-301.7701-b-1` | 1,670 | - | - | not added by p2 ingest |
| `cfr26-31.3121-b-19-1` | 658 | - | - | not added by p2 ingest |
| `cfr8-212.0` | 216 | - | - | not added by p2 ingest |
| `cfr8-212.1-p01-documentary-requirements-for` | 1,401 | - | - | not added by p2 ingest |
| `cfr8-212.1-p02-documentary-requirements-for` | 1,409 | - | - | not added by p2 ingest |
| `cfr8-212.1-p03-documentary-requirements-for` | 1,164 | - | - | not added by p2 ingest |
| `cfr8-212.1-p04-documentary-requirements-for` | 1,293 | - | - | not added by p2 ingest |
| `cfr8-212.1-p05-documentary-requirements-for` | 1,360 | - | - | not added by p2 ingest |
| `cfr8-212.1-p06-documentary-requirements-for` | 1,101 | - | - | not added by p2 ingest |
| `cfr8-212.1-p07-documentary-requirements-for` | 1,210 | - | - | not added by p2 ingest |
| `cfr8-212.1-p08-documentary-requirements-for` | 381 | - | - | not added by p2 ingest |
| `cfr8-212.10` | 81 | - | - | not added by p2 ingest |
| `cfr8-212.12` | 1,503 | - | - | not added by p2 ingest |
| `cfr8-212.14` | 1,131 | - | - | not added by p2 ingest |
| `cfr8-212.15-p01-certificates-for-foreign-hea` | 1,327 | - | - | not added by p2 ingest |
| `cfr8-212.15-p02-certificates-for-foreign-hea` | 1,327 | - | - | not added by p2 ingest |
| `cfr8-212.15-p03-certificates-for-foreign-hea` | 1,379 | - | - | not added by p2 ingest |
| `cfr8-212.15-p04-certificates-for-foreign-hea` | 1,492 | - | - | not added by p2 ingest |
| `cfr8-212.15-p05-certificates-for-foreign-hea` | 393 | - | - | not added by p2 ingest |
| `cfr8-212.16` | 394 | - | - | not added by p2 ingest |
| `cfr8-212.17` | 417 | - | - | not added by p2 ingest |
| `cfr8-212.18` | 292 | - | - | not added by p2 ingest |
| `cfr8-212.19-p01-parole-for-entrepreneurs` | 1,505 | - | - | not added by p2 ingest |
| `cfr8-212.19-p02-parole-for-entrepreneurs` | 1,459 | - | - | not added by p2 ingest |
| `cfr8-212.19-p03-parole-for-entrepreneurs` | 368 | - | - | not added by p2 ingest |
| `cfr8-212.2` | 1,377 | - | - | not added by p2 ingest |
| `cfr8-212.3` | 751 | - | - | not added by p2 ingest |
| `cfr8-212.4-p01-applications-for-the-exercis` | 1,495 | - | - | not added by p2 ingest |
| `cfr8-212.4-p02-applications-for-the-exercis` | 1,466 | - | - | not added by p2 ingest |
| `cfr8-212.4-p03-applications-for-the-exercis` | 488 | - | - | not added by p2 ingest |
| `cfr8-212.5` | 1,562 | - | - | not added by p2 ingest |
| `cfr8-212.6` | 1,297 | - | - | not added by p2 ingest |
| `cfr8-212.7-p01-waiver-of-certain-grounds-of` | 1,391 | - | - | not added by p2 ingest |
| `cfr8-212.7-p02-waiver-of-certain-grounds-of` | 1,149 | - | - | not added by p2 ingest |
| `cfr8-212.7-p03-waiver-of-certain-grounds-of` | 827 | - | - | not added by p2 ingest |
| `cfr8-212.7-p04-waiver-of-certain-grounds-of` | 1,400 | - | - | not added by p2 ingest |
| `cfr8-212.7-p05-waiver-of-certain-grounds-of` | 677 | - | - | not added by p2 ingest |
| `cfr8-212.7-p06-waiver-of-certain-grounds-of` | 1,484 | - | - | not added by p2 ingest |
| `cfr8-214.1-p01-general` | 1,284 | - | - | not added by p2 ingest |
| `cfr8-214.1-p02-aliens-applying-for-admission` | 2,290 | - | - | not added by p2 ingest |
| `cfr8-214.1-p03-termination-of-status-through` | 1,366 | - | - | not added by p2 ingest |
| `cfr8-214.1-p04-period-of-stay-through` | 1,469 | - | - | not added by p2 ingest |
| `cfr8-214.13` | 1,858 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p01-students-in-colleges-universit` | 759 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p02-period-of-stay` | 2,287 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p03-full-course-of-study` | 1,637 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p04-extension-of-stay-through` | 1,706 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p05-employment` | 1,174 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p06-practical-training-through-cur` | 429 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p07-general-through-24-month` | 2,520 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p08-extension-of-stay-for` | 1,529 | - | - | not added by p2 ingest |
| `cfr8-214.2-f-p09-temporary-absence-from-the` | 1,565 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p01-temporary-employees-through-ad` | 782 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p02-petitions-through-h-1b` | 1,659 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p03-h-2a-and-h` | 966 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p04-petition-for-registered-nurse` | 831 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p05-petition-for-alien-to` | 1,661 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p06-general-h-1b-requirements` | 1,489 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p07-licensure-for-h-classification` | 1,432 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p08-criteria-and-documentary-requi` | 327 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p09-petition-for-alien-to` | 1,809 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p10-validity-through-treatment-of` | 2,031 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p11-petition-for-alien-to` | 1,560 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p12-temporary-services-or-labor` | 1,962 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p13-evidence-for-h-2b` | 1,252 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p14-special-requirements-for-addit` | 1,810 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p15-special-requirements-for-addit` | 1,848 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p16-petition-for-alien-trainee` | 929 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p17-numerical-limits-through-proce` | 395 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p18-registration` | 1,980 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p19-confirmation-through-cap-exemp` | 1,409 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p20-suspension-of-registration-req` | 1,254 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p21-h-1c-numerical-limitations` | 668 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p22-approval-and-validity-of` | 1,300 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p23-denial-of-petition` | 1,504 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p24-revocation-of-approval-of` | 862 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p25-admission-through-h-1b` | 2,383 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p26-h-3-limitation-on` | 1,603 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p27-use-of-approval-notice` | 1,369 | - | - | not added by p2 ingest |
| `cfr8-214.2-h-p28-severability-through-severabil` | 1,501 | - | - | not added by p2 ingest |
| `cfr8-214.2-j-p01-eligibility-for-admission-thro` | 1,379 | - | - | not added by p2 ingest |
| `cfr8-214.2-j-p02-employment-of-j-2` | 1,244 | - | - | not added by p2 ingest |
| `cfr8-214.2-j-p03-special-reporting-requirement` | 588 | - | - | not added by p2 ingest |
| `cfr8-214.3-p01-filing-petition-through-suppor` | 1,309 | - | - | not added by p2 ingest |
| `cfr8-214.3-p02-additional-evidence-through-re` | 2,457 | - | - | not added by p2 ingest |
| `cfr8-214.3-p03-sevp-certification-recertifica` | 1,570 | - | - | not added by p2 ingest |
| `cfr8-214.3-p04-administration-of-student-regu` | 854 | - | - | not added by p2 ingest |
| `cfr8-214.4` | 1,874 | - | - | not added by p2 ingest |
| `cfr8-245.1-p01-eligibility` | 1,390 | - | - | not added by p2 ingest |
| `cfr8-245.1-p02-eligibility` | 1,481 | - | - | not added by p2 ingest |
| `cfr8-245.1-p03-eligibility` | 1,345 | - | - | not added by p2 ingest |
| `cfr8-245.10` | 2,768 | - | - | not added by p2 ingest |
| `cfr8-245.11` | 1,998 | - | - | not added by p2 ingest |
| `cfr8-245.15-p01-adjustment-of-status-of-cert` | 1,363 | - | - | not added by p2 ingest |
| `cfr8-245.15-p02-adjustment-of-status-of-cert` | 1,236 | - | - | not added by p2 ingest |
| `cfr8-245.15-p03-adjustment-of-status-of-cert` | 1,447 | - | - | not added by p2 ingest |
| `cfr8-245.15-p04-adjustment-of-status-of-cert` | 1,382 | - | - | not added by p2 ingest |
| `cfr8-245.15-p05-adjustment-of-status-of-cert` | 1,386 | - | - | not added by p2 ingest |
| `cfr8-245.15-p06-adjustment-of-status-of-cert` | 1,380 | - | - | not added by p2 ingest |
| `cfr8-245.18` | 1,701 | - | - | not added by p2 ingest |
| `cfr8-245.2` | 1,961 | - | - | not added by p2 ingest |
| `cfr8-245.21` | 1,167 | - | - | not added by p2 ingest |
| `cfr8-245.22` | 751 | - | - | not added by p2 ingest |
| `cfr8-245.23` | 2,663 | - | - | not added by p2 ingest |
| `cfr8-245.24-p01-adjustment-of-aliens-in-u-no` | 1,492 | - | - | not added by p2 ingest |
| `cfr8-245.24-p02-adjustment-of-aliens-in-u-no` | 1,250 | - | - | not added by p2 ingest |
| `cfr8-245.24-p03-adjustment-of-aliens-in-u-no` | 1,004 | - | - | not added by p2 ingest |
| `cfr8-245.25` | 524 | - | - | not added by p2 ingest |
| `cfr8-245.3` | 362 | - | - | not added by p2 ingest |
| `cfr8-245.4` | 106 | - | - | not added by p2 ingest |
| `cfr8-245.5` | 219 | - | - | not added by p2 ingest |
| `cfr8-245.6` | 76 | - | - | not added by p2 ingest |
| `cfr8-245.7` | 445 | - | - | not added by p2 ingest |
| `cfr8-245.8` | 588 | - | - | not added by p2 ingest |
| `cfr8-248.1` | 900 | - | - | not added by p2 ingest |
| `cfr8-248.2` | 452 | - | - | not added by p2 ingest |
| `cfr8-248.3` | 1,020 | - | - | not added by p2 ingest |
| `cfr8-265.1` | 63 | - | - | not added by p2 ingest |
| `cfr8-274a.1` | 999 | - | - | not added by p2 ingest |
| `cfr8-274a.12-p01-aliens-authorized-employment-i` | 892 | - | - | not added by p2 ingest |
| `cfr8-274a.12-p02-aliens-authorized-for-employme` | 1,279 | - | - | not added by p2 ingest |
| `cfr8-274a.12-p03-an-international-cultural-exch` | 1,275 | - | - | not added by p2 ingest |
| `cfr8-274a.12-p04-reserved-through-aliens-who` | 2,121 | - | - | not added by p2 ingest |
| `cfr8-274a.12-p05-an-alien-lawfully-enlisted` | 319 | - | - | not added by p2 ingest |
| `cfr8-274a.13` | 1,205 | - | - | not added by p2 ingest |
| `cfr8-274a.14` | 520 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p01-general` | 350 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p02-examination-of-documents-and` | 1,504 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p03-in-the-case-of` | 1,688 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p04-retention-and-inspection-of` | 1,056 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p05-employment-verification-requir` | 1,498 | - | - | not added by p2 ingest |
| `cfr8-274a.2-p06-documentation-through-electron` | 681 | - | - | not added by p2 ingest |
| `dol-eta-h1b` | 837 | - | - | not added by p2 ingest |
| `dol-eta-prevailing-wages` | 1,100 | - | - | not added by p2 ingest |
| `dol-whd-flsa-misclassification` | 284 | - | - | not added by p2 ingest |
| `dol-whd-fs-13-flsa-employment-relationship-p01-fact-sheet-13-employee` | 698 | - | - | not added by p2 ingest |
| `dol-whd-fs-13-flsa-employment-relationship-p02-economic-reality-test-factors` | 2,239 | - | - | not added by p2 ingest |
| `dol-whd-fs-14-flsa-coverage` | 381 | - | - | not added by p2 ingest |
| `dol-whd-fs-15-tipped-employees-flsa` | 2,356 | - | - | not added by p2 ingest |
| `dol-whd-fs-16-flsa-wage-deductions` | 688 | - | - | not added by p2 ingest |
| `dol-whd-fs-17s-overtime-educational-institutions` | 2,194 | - | - | not added by p2 ingest |
| `dol-whd-fs-21-flsa-recordkeeping` | 729 | - | - | not added by p2 ingest |
| `dol-whd-fs-22-flsa-hours-worked` | 1,074 | - | - | not added by p2 ingest |
| `dol-whd-fs-23-flsa-overtime-pay` | 886 | - | - | not added by p2 ingest |
| `dol-whd-fs-48-hoffman-plastics` | 564 | - | - | not added by p2 ingest |
| `dol-whd-fs-62-index-h1b` | 647 | - | - | not added by p2 ingest |
| `dol-whd-fs-62b-h1b-employer` | 466 | - | - | not added by p2 ingest |
| `dol-whd-fs-62g-h1b-required-wage` | 585 | - | - | not added by p2 ingest |
| `dol-whd-fs-62h-h1b-pay-deductions` | 433 | - | - | not added by p2 ingest |
| `dol-whd-fs-62i-h1b-nonproductive-time` | 583 | - | - | not added by p2 ingest |
| `dol-whd-fs-62m-h1b-notice` | 491 | - | - | not added by p2 ingest |
| `dol-whd-fs-62q-h1b-exempt-workers` | 694 | - | - | not added by p2 ingest |
| `dol-whd-fs-62r-h1b-whistleblowers` | 340 | - | - | not added by p2 ingest |
| `dol-whd-fs-62w-h1b-portability` | 326 | - | - | not added by p2 ingest |
| `dol-whd-fs-65-flsa-student-learners` | 372 | - | - | not added by p2 ingest |
| `dol-whd-fs-68-h1b-fulltime-employee` | 359 | - | - | not added by p2 ingest |
| `dol-whd-fs-71-flsa-internships` | 617 | - | - | not added by p2 ingest |
| `dol-whd-fs-77a-flsa-prohibiting-retaliation` | 408 | - | - | not added by p2 ingest |
| `dol-whd-handy-reference-guide-flsa-p01-handy-reference-guide-to` | 1,321 | - | - | not added by p2 ingest |
| `dol-whd-handy-reference-guide-flsa-p02-youth-minimum-wage-through` | 1,275 | - | - | not added by p2 ingest |
| `dol-whd-handy-reference-guide-flsa-p03-nursing-employees-through-comp` | 1,369 | - | - | not added by p2 ingest |
| `dol-whd-handy-reference-guide-flsa-p04-enforcement-through-investigat` | 1,310 | - | - | not added by p2 ingest |
| `dol-whd-immigration-h1b` | 782 | - | - | not added by p2 ingest |
| `fincen-fbar` | 154 | - | - | not added by p2 ingest |
| `ice-sevis` | 685 | - | - | not added by p2 ingest |
| `irs-alien-liability-for-social-security-and-medicare-taxes-of-foreign-teac` | 1,088 | - | - | not added by p2 ingest |
| `irs-aliens-employed-in-the-us` | 969 | - | - | not added by p2 ingest |
| `irs-aliens-employed-in-the-us-social-security-taxes` | 929 | - | - | not added by p2 ingest |
| `irs-claiming-tax-treaty-benefits` | 1,518 | - | - | not added by p2 ingest |
| `irs-claiming-treaty-exemption-for-a-scholarship-or-fellowship-grant` | 973 | - | - | not added by p2 ingest |
| `irs-closer-connection-exception-to-the-substantial-presence-test` | 1,043 | - | - | not added by p2 ingest |
| `irs-delays-in-issuing-ssns-to-aliens-by-the-social-security-administration` | 614 | - | - | not added by p2 ingest |
| `irs-departing-alien-clearance-sailing-permit` | 2,415 | - | - | not added by p2 ingest |
| `irs-dual-status-individuals` | 289 | - | - | not added by p2 ingest |
| `irs-exempt-individual-who-is-a-student` | 440 | - | - | not added by p2 ingest |
| `irs-exempt-individuals-teachers-and-trainees` | 449 | - | - | not added by p2 ingest |
| `irs-federal-income-tax-reporting-and-withholding-on-wages-paid-to-aliens` | 1,057 | - | - | not added by p2 ingest |
| `irs-federal-income-tax-withholding-and-reporting-on-other-kinds-of-us-sour` | 2,059 | - | - | not added by p2 ingest |
| `irs-foreign-student-liability-for-social-security-and-medicare-taxes` | 859 | - | - | not added by p2 ingest |
| `irs-foreign-students-and-scholars` | 519 | - | - | not added by p2 ingest |
| `irs-form-8938-fbar-comparison` | 1,339 | - | - | not added by p2 ingest |
| `irs-frequently-asked-questions-about-international-individual-tax-matters-p01-frequently-asked-questions-abo` | 1,281 | - | - | not added by p2 ingest |
| `irs-frequently-asked-questions-about-international-individual-tax-matters-p02-filing-status-and-dependents` | 1,463 | - | - | not added by p2 ingest |
| `irs-frequently-asked-questions-about-international-individual-tax-matters-p03-expatriation-former-citizens-a` | 2,074 | - | - | not added by p2 ingest |
| `irs-frequently-asked-questions-about-international-individual-tax-matters-p04-reporting-of-foreign-financial` | 1,631 | - | - | not added by p2 ingest |
| `irs-frequently-asked-questions-about-international-individual-tax-matters-p05-foreign-earned-income-exclusio` | 1,268 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p01-u-s-nonresident-alien` | 2,049 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p02-affordable-care-act-what` | 1,253 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p03-reminders` | 360 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p04-filing-requirements-through-do` | 1,326 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p05-exception-1-through-signature` | 1,436 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p06-additional-information-through` | 1,346 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p07-substantial-presence-test-thro` | 1,390 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p08-where-to-file-through` | 1,457 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p09-how-to-figure-tax` | 1,575 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p10-foreign-income-taxed-by` | 1,504 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p11-digital-assets-through-fringe` | 1,285 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p12-missing-or-incorrect-form` | 1,302 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p13-fully-taxable-pensions-and` | 1,330 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p14-schedule-j-form-1040` | 1,280 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p15-line-35e-through-how` | 1,325 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p16-innocent-spouse-relief-through` | 352 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p17-how-to-get-tax` | 2,525 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p18-the-taxpayer-advocate-service` | 1,347 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p19-line-6-farm-income` | 1,515 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p20-line-8s-nontaxable-amount` | 1,318 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p21-line-24f-contributions-to` | 1,423 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p22-line-4-self-employment` | 1,290 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p23-line-17p-any-interest` | 1,289 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p24-line-9-net-premium` | 2,183 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p25-line-2-gifts-by` | 1,352 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p26-other-itemized-deductions-thro` | 1,367 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p27-exceptions-through-lines-16` | 1,356 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p28-instructions-for-schedule-oi` | 1,289 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p29-line-e-total-through` | 1,318 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p30-how-to-complete-the` | 1,299 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p31-line-9-through-disclosure` | 1,625 | - | - | not added by p2 ingest |
| `irs-instr-1040nr-p32-we-welcome-comments-on` | 1,222 | - | - | not added by p2 ingest |
| `irs-instr-w7-p01-application-for-irs-individual` | 961 | - | - | not added by p2 ingest |
| `irs-instr-w7-p02-general-instructions-through-c` | 1,410 | - | - | not added by p2 ingest |
| `irs-instr-w7-p03-who-is-eligible-to` | 1,304 | - | - | not added by p2 ingest |
| `irs-instr-w7-p04-additional-documentation-requi` | 1,701 | - | - | not added by p2 ingest |
| `irs-instr-w7-p05-when-to-apply-through` | 884 | - | - | not added by p2 ingest |
| `irs-instr-w7-p06-specific-instructions-through` | 1,782 | - | - | not added by p2 ingest |
| `irs-instr-w7-p07-exception-1-passive-income` | 2,005 | - | - | not added by p2 ingest |
| `irs-instr-w7-p08-signature-through-acceptance-a` | 471 | - | - | not added by p2 ingest |
| `irs-instr-w7-p09-through-exceptions-tables` | 2,526 | - | - | not added by p2 ingest |
| `irs-instr-w7-p10-exception-4` | 883 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p01-certificate-of-foreign-status` | 645 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p02-general-instructions-through-d` | 2,021 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p03-definitions` | 2,421 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p04-specific-instructions-through` | 1,341 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p05-part-ii-through-nonresident` | 1,415 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p06-part-iii-through-certification` | 474 | - | - | not added by p2 ingest |
| `irs-instr-w8ben-p07-paperwork-reduction-act-notice` | 289 | - | - | not added by p2 ingest |
| `irs-introduction-to-residency-under-us-tax-law` | 454 | - | - | not added by p2 ingest |
| `irs-itin-documentation-frequently-asked-questions-faqs` | 547 | - | - | not added by p2 ingest |
| `irs-nonresident-alien-students-and-the-tax-home-concept` | 978 | - | - | not added by p2 ingest |
| `irs-nonresident-aliens` | 753 | - | - | not added by p2 ingest |
| `irs-nonresident-aliens-dependents` | 398 | - | - | not added by p2 ingest |
| `irs-nonresident-aliens-exclusions-from-income` | 1,030 | - | - | not added by p2 ingest |
| `irs-nonresident-figuring-your-tax` | 988 | - | - | not added by p2 ingest |
| `irs-nonresident-spouse` | 1,262 | - | - | not added by p2 ingest |
| `irs-obtaining-an-itin-from-abroad` | 315 | - | - | not added by p2 ingest |
| `irs-pub-519-p01-through-reminders` | 1,826 | - | - | not added by p2 ingest |
| `irs-pub-519-p02-1-nonresident-alien-or` | 1,119 | - | - | not added by p2 ingest |
| `irs-pub-519-p03-regular-commuters-from-canada` | 2,551 | - | - | not added by p2 ingest |
| `irs-pub-519-p04-days-of-presence-in` | 1,501 | - | - | not added by p2 ingest |
| `irs-pub-519-p05-dual-status-aliens-through` | 1,914 | - | - | not added by p2 ingest |
| `irs-pub-519-p06-choosing-resident-alien-status` | 1,560 | - | - | not added by p2 ingest |
| `irs-pub-519-p07-nonresident-spouse-treated-as` | 1,280 | - | - | not added by p2 ingest |
| `irs-pub-519-p08-aliens-from-american-samoa` | 1,502 | - | - | not added by p2 ingest |
| `irs-pub-519-p09-guarantee-of-indebtedness-thro` | 1,885 | - | - | not added by p2 ingest |
| `irs-pub-519-p10-alternative-basis-through-pers` | 2,015 | - | - | not added by p2 ingest |
| `irs-pub-519-p11-community-income` | 356 | - | - | not added by p2 ingest |
| `irs-pub-519-p12-3-exclusions-from-gross` | 1,333 | - | - | not added by p2 ingest |
| `irs-pub-519-p13-dividend-income-through-servic` | 1,278 | - | - | not added by p2 ingest |
| `irs-pub-519-p14-gambling-winnings-from-dog` | 749 | - | - | not added by p2 ingest |
| `irs-pub-519-p15-4-how-income-of` | 1,674 | - | - | not added by p2 ingest |
| `irs-pub-519-p16-personal-services-income-throu` | 1,863 | - | - | not added by p2 ingest |
| `irs-pub-519-p17-gain-or-loss-of` | 1,579 | - | - | not added by p2 ingest |
| `irs-pub-519-p18-gambling-winnings-through-inco` | 1,824 | - | - | not added by p2 ingest |
| `irs-pub-519-p19-transportation-tax-through-how` | 1,358 | - | - | not added by p2 ingest |
| `irs-pub-519-p20-expatriation-tax-return-throug` | 1,482 | - | - | not added by p2 ingest |
| `irs-pub-519-p21-nonresident-aliens-through-non` | 1,707 | - | - | not added by p2 ingest |
| `irs-pub-519-p22-dependents-through-nonresident` | 1,888 | - | - | not added by p2 ingest |
| `irs-pub-519-p23-tax-credits-and-payments` | 1,268 | - | - | not added by p2 ingest |
| `irs-pub-519-p24-credits` | 1,450 | - | - | not added by p2 ingest |
| `irs-pub-519-p25-tax-withheld-through-bona` | 1,454 | - | - | not added by p2 ingest |
| `irs-pub-519-p26-6-dual-status-tax` | 1,483 | - | - | not added by p2 ingest |
| `irs-pub-519-p27-tax-credits-and-payments` | 1,422 | - | - | not added by p2 ingest |
| `irs-pub-519-p28-when-and-where-to` | 355 | - | - | not added by p2 ingest |
| `irs-pub-519-p29-7-filing-information-through` | 1,297 | - | - | not added by p2 ingest |
| `irs-pub-519-p30-when-to-file-through` | 1,452 | - | - | not added by p2 ingest |
| `irs-pub-519-p31-form-8938-through-civil` | 1,994 | - | - | not added by p2 ingest |
| `irs-pub-519-p32-criminal-penalties-through-wag` | 1,547 | - | - | not added by p2 ingest |
| `irs-pub-519-p33-withholding-on-pensions-throug` | 1,573 | - | - | not added by p2 ingest |
| `irs-pub-519-p34-withholding-from-other-income` | 1,340 | - | - | not added by p2 ingest |
| `irs-pub-519-p35-income-entitled-to-tax` | 1,796 | - | - | not added by p2 ingest |
| `irs-pub-519-p36-students-and-exchange-visitors` | 1,687 | - | - | not added by p2 ingest |
| `irs-pub-519-p37-international-social-security` | 1,369 | - | - | not added by p2 ingest |
| `irs-pub-519-p38-9-tax-treaty-benefits` | 1,256 | - | - | not added by p2 ingest |
| `irs-pub-519-p39-teachers-professors-and-resear` | 1,537 | - | - | not added by p2 ingest |
| `irs-pub-519-p40-reporting-treaty-benefits-clai` | 557 | - | - | not added by p2 ingest |
| `irs-pub-519-p41-10-employees-of-foreign` | 1,520 | - | - | not added by p2 ingest |
| `irs-pub-519-p42-11-departing-aliens-and` | 1,441 | - | - | not added by p2 ingest |
| `irs-pub-519-p43-12-how-to-get` | 2,575 | - | - | not added by p2 ingest |
| `irs-pub-519-p44-the-taxpayer-advocate-service` | 622 | - | - | not added by p2 ingest |
| `irs-pub-519-p45-through-frequently-asked-quest` | 508 | - | - | not added by p2 ingest |
| `irs-pub-519-p46-what-is-the-difference` | 3,682 | - | - | not added by p2 ingest |
| `irs-pub-519-p47-i-am-a-student` | 2,976 | - | - | not added by p2 ingest |
| `irs-pub-519-p48-i-am-a-nonresident` | 2,811 | - | - | not added by p2 ingest |
| `irs-pub-519-p49-when-is-my-form` | 3,373 | - | - | not added by p2 ingest |
| `irs-pub-519-p50-i-have-an-h` | 2,667 | - | - | not added by p2 ingest |
| `irs-pub-519-p51-i-am-a-nonresident` | 2,521 | - | - | not added by p2 ingest |
| `irs-pub-519-p52-i-am-single-with` | 1,462 | - | - | not added by p2 ingest |
| `irs-pub-519-p53-appendix-a-tax-treaty` | 1,352 | - | - | not added by p2 ingest |
| `irs-pub-519-p54-france-through-korea-norway` | 1,413 | - | - | not added by p2 ingest |
| `irs-pub-519-p55-morocco-through-trinidad-and` | 1,253 | - | - | not added by p2 ingest |
| `irs-pub-519-p56-tunisia-through-czech-republic` | 1,504 | - | - | not added by p2 ingest |
| `irs-pub-519-p57-egypt-korea-philippines-poland` | 1,257 | - | - | not added by p2 ingest |
| `irs-pub-519-p58-indonesia-through-netherlands` | 1,465 | - | - | not added by p2 ingest |
| `irs-pub-519-p59-norway-through-trinidad-and` | 1,509 | - | - | not added by p2 ingest |
| `irs-pub-519-p60-united-kingdom` | 298 | - | - | not added by p2 ingest |
| `irs-pub-901-p01-future-developments-reminders` | 875 | - | - | not added by p2 ingest |
| `irs-pub-901-p02-through-tax-exemptions-provide` | 588 | - | - | not added by p2 ingest |
| `irs-pub-901-p03-personal-services-income-throu` | 1,497 | - | - | not added by p2 ingest |
| `irs-pub-901-p04-belgium-through-chile` | 1,294 | - | - | not added by p2 ingest |
| `irs-pub-901-p05-china-people-s-republic` | 1,366 | - | - | not added by p2 ingest |
| `irs-pub-901-p06-egypt-through-germany` | 1,530 | - | - | not added by p2 ingest |
| `irs-pub-901-p07-greece-through-ireland` | 1,389 | - | - | not added by p2 ingest |
| `irs-pub-901-p08-israel-through-japan` | 1,284 | - | - | not added by p2 ingest |
| `irs-pub-901-p09-kazakhstan-through-lithuania` | 1,240 | - | - | not added by p2 ingest |
| `irs-pub-901-p10-luxembourg-through-morocco` | 1,271 | - | - | not added by p2 ingest |
| `irs-pub-901-p11-netherlands-through-philippine` | 1,276 | - | - | not added by p2 ingest |
| `irs-pub-901-p12-poland-through-russia` | 1,247 | - | - | not added by p2 ingest |
| `irs-pub-901-p13-slovak-republic-through-spain` | 1,362 | - | - | not added by p2 ingest |
| `irs-pub-901-p14-sri-lanka-through-thailand` | 1,383 | - | - | not added by p2 ingest |
| `irs-pub-901-p15-trinidad-and-tobago-through` | 1,535 | - | - | not added by p2 ingest |
| `irs-pub-901-p16-venezuela` | 358 | - | - | not added by p2 ingest |
| `irs-pub-901-p17-professors-teachers-and-resear` | 1,365 | - | - | not added by p2 ingest |
| `irs-pub-901-p18-germany-through-netherlands` | 1,340 | - | - | not added by p2 ingest |
| `irs-pub-901-p19-norway-through-trinidad-and` | 1,292 | - | - | not added by p2 ingest |
| `irs-pub-901-p20-turkey-through-venezuela` | 310 | - | - | not added by p2 ingest |
| `irs-pub-901-p21-students-and-apprentices-throu` | 1,290 | - | - | not added by p2 ingest |
| `irs-pub-901-p22-commonwealth-of-independent-st` | 1,431 | - | - | not added by p2 ingest |
| `irs-pub-901-p23-estonia-through-iceland` | 1,286 | - | - | not added by p2 ingest |
| `irs-pub-901-p24-india-through-kazakhstan` | 1,322 | - | - | not added by p2 ingest |
| `irs-pub-901-p25-korea-south-through-mexico` | 1,244 | - | - | not added by p2 ingest |
| `irs-pub-901-p26-morocco-through-philippines` | 1,342 | - | - | not added by p2 ingest |
| `irs-pub-901-p27-poland-through-slovak-republic` | 1,492 | - | - | not added by p2 ingest |
| `irs-pub-901-p28-slovenia-through-thailand` | 1,340 | - | - | not added by p2 ingest |
| `irs-pub-901-p29-trinidad-and-tobago-through` | 1,075 | - | - | not added by p2 ingest |
| `irs-pub-901-p30-wages-and-pensions-paid` | 1,345 | - | - | not added by p2 ingest |
| `irs-pub-901-p31-commonwealth-of-independent-st` | 1,272 | - | - | not added by p2 ingest |
| `irs-pub-901-p32-india-through-latvia` | 1,274 | - | - | not added by p2 ingest |
| `irs-pub-901-p33-lithuania-through-poland` | 1,265 | - | - | not added by p2 ingest |
| `irs-pub-901-p34-portugal-through-switzerland` | 1,253 | - | - | not added by p2 ingest |
| `irs-pub-901-p35-thailand-through-venezuela` | 911 | - | - | not added by p2 ingest |
| `irs-pub-901-p36-how-to-get-tax` | 2,551 | - | - | not added by p2 ingest |
| `irs-pub-901-p37-through-taxpayer-assistance-ou` | 838 | - | - | not added by p2 ingest |
| `irs-residency-starting-and-ending-dates` | 1,927 | - | - | not added by p2 ingest |
| `irs-source-of-income-personal-service-income` | 1,118 | - | - | not added by p2 ingest |
| `irs-student-fica-exception` | 969 | - | - | not added by p2 ingest |
| `irs-substantial-presence-test` | 820 | - | - | not added by p2 ingest |
| `irs-tax-residency-status-examples-p01-tax-residency-status-examples` | 1,405 | - | - | not added by p2 ingest |
| `irs-tax-residency-status-examples-p02-analysis-for-2023-through` | 1,566 | - | - | not added by p2 ingest |
| `irs-tax-residency-status-examples-p03-analysis-for-2024-through` | 1,524 | - | - | not added by p2 ingest |
| `irs-tax-residency-status-examples-p04-analysis-for-2025-through` | 288 | - | - | not added by p2 ingest |
| `irs-tax-residency-status-first-year-choice` | 912 | - | - | not added by p2 ingest |
| `irs-tax-treaty-tables` | 1,027 | - | - | not added by p2 ingest |
| `irs-taxation-of-aliens-by-visa-type-and-immigration-status` | 619 | - | - | not added by p2 ingest |
| `irs-taxation-of-dual-status-individuals` | 1,438 | - | - | not added by p2 ingest |
| `irs-taxation-of-nonresident-aliens` | 1,004 | - | - | not added by p2 ingest |
| `irs-taxpayer-identification-numbers-tins-for-foreign-students-and-scholars` | 220 | - | - | not added by p2 ingest |
| `irs-the-closer-connection-exception-to-the-substantial-presence-test-for-f` | 415 | - | - | not added by p2 ingest |
| `irs-the-taxation-of-capital-gains-of-nonresident-students-scholars-and-emp` | 837 | - | - | not added by p2 ingest |
| `irs-topic-851` | 2,039 | - | - | not added by p2 ingest |
| `irs-topic-857` | 1,388 | - | - | not added by p2 ingest |
| `irs-totalization-agreements` | 1,317 | - | - | not added by p2 ingest |
| `irs-withholding-certificate-and-exemption-for-nonresident-alien-employees` | 630 | - | - | not added by p2 ingest |
| `irs-withholding-certificates-and-exemptions-for-personal-services-and-stud` | 516 | - | - | not added by p2 ingest |
| `irs-withholding-federal-income-tax-on-scholarships-fellowships-and-grants` | 390 | - | - | not added by p2 ingest |
| `sevp-maintaining-status` | 1,117 | - | - | not added by p2 ingest |
| `sevp-transferring-schools` | 294 | - | - | not added by p2 ingest |
| `sevp-traveling-f-m` | 535 | - | - | not added by p2 ingest |
| `state-j2-visa` | 338 | - | - | not added by p2 ingest |
| `uscis-eb-1` | 1,044 | - | - | not added by p2 ingest |
| `uscis-eb-2-p01-you-may-be-eligible-for-an-e` | 1,083 | - | - | not added by p2 ingest |
| `uscis-eb-2-p02-national-interest-waiver-fil` | 2,055 | - | - | not added by p2 ingest |
| `uscis-eb-3` | 731 | - | - | not added by p2 ingest |
| `uscis-h4-ead` | 1,485 | - | - | not added by p2 ingest |
| `uscis-i-765-p01-certain-aliens-who-are-in-th` | 281 | - | - | not added by p2 ingest |
| `uscis-i-765-p02-form-details` | 3,055 | - | - | not added by p2 ingest |
| `uscis-l-1a` | 1,402 | - | - | not added by p2 ingest |
| `uscis-l-1b` | 1,473 | - | - | not added by p2 ingest |
| `uscis-o-1` | 2,181 | - | - | not added by p2 ingest |
| `uscis-opt-f1` | 1,265 | - | - | not added by p2 ingest |
| `uscis-permanent-workers` | 727 | - | - | not added by p2 ingest |
| `uscis-policy-manual-v8-o` | 949 | - | - | not added by p2 ingest |
| `uscis-stem-opt` | 1,794 | - | - | not added by p2 ingest |
| `uscis-students-and-employment` | 545 | - | - | not added by p2 ingest |
| `uscis-tn` | 891 | - | - | not added by p2 ingest |
| `uscis-unlawful-presence` | 1,844 | - | - | not added by p2 ingest |
| `uscode-8-1182__p001-005` | 4,189 | - | - | not added by p2 ingest |
| `uscode-8-1182__p006-010` | 4,216 | - | - | not added by p2 ingest |
| `uscode-8-1182__p011-015` | 5,285 | - | - | not added by p2 ingest |
| `uscode-8-1182__p016-020` | 5,117 | - | - | not added by p2 ingest |
| `uscode-8-1182__p021-025` | 5,035 | - | - | not added by p2 ingest |
| `uscode-8-1182__p026-030` | 5,858 | - | - | not added by p2 ingest |
| `uscode-8-1182__p031-035` | 6,396 | - | - | not added by p2 ingest |
| `uscode-8-1182__p036-040` | 6,802 | - | - | not added by p2 ingest |
| `uscode-8-1182__p041-045` | 6,193 | - | - | not added by p2 ingest |
| `uscode-8-1182__p046-050` | 6,182 | - | - | not added by p2 ingest |
| `uscode-8-1182__p051-055` | 6,528 | - | - | not added by p2 ingest |
| `uscode-8-1182__p056-059` | 4,902 | - | - | not added by p2 ingest |

## Not added in the last run

Nothing was left out.

## What to check by eye

Ingest cleans text by rules, and rules miss things.
Take five minutes to open the shortest, a middle one and the longest document next to its original and read one page of each.

- Search the documents for `þ`, `¼`, `(cid:` and the replacement character.
  A hit usually means the PDF's font map is wrong, which no tool can repair, so treat it as a defect and leave that document out.
- Look at the end of a few papers.
  Ingest drops a trailing reference list when it finds a References heading or a run of numbered entries.
  A paper whose list has neither can keep it, and then every author and journal name matches queries it should not.
- Open the first lines of a few documents.
  Author lists, copyright pages and tables of contents are not removed automatically, and you may want to cut them.
- Compare one table with the PDF.
  A PDF prints footnote marks as small raised digits, and the converter glues them onto the word or number next to them: `ALUMINUM1` is the heading ALUMINUM with footnote 1, and `11210,000` can be 210,000 with footnote 11.
  Quotes still match the stored text, but a number read from it can be wrong, so check before you trust a figure in a query, a judgment or an answer.
- Fix the `license` column in the manifest for every document, then run `uv run p2 license`.
  It is `unknown` until you do, and `unknown` does not pass.

## If a document is flagged as scanned

A scan is a picture of a page, so there is no text for ingest to read.
This template does not install an OCR tool, because it is large and most students never need it.
If you do need one, the opt-in route is pymupdf4llm with rapidocr, run on its own outside the template's environment:

```
uv run --no-project --with pymupdf4llm --with rapidocr python -c "import pymupdf4llm, sys, pathlib; pathlib.Path(sys.argv[2]).write_text(pymupdf4llm.to_markdown(sys.argv[1], use_ocr=True, force_ocr=True), encoding='utf-8')" scan.pdf scan.md
```

Put the resulting `.md` file in your folder and ingest the folder again.
It costs about 2 seconds a page, and OCR text needs a second look: it misreads ligatures, hyphens and numbers.
pymupdf4llm is AGPL-3.0 software, so use it only as a tool on your own machine, and do not add it to this repo's dependencies or copy its code into the repo.
