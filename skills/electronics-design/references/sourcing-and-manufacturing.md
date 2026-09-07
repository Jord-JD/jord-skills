# Sourcing and manufacturing

Read this when selecting purchasable components, choosing fabrication specifications, reducing board cost, or preparing supplier quotations. Use current manufacturer and supplier information; keep dated findings in the project rather than embedding prices or stock counts in this skill.

## Source parts before committing to layout

For each production BOM line, record the exact manufacturer and ordering code, package, lifecycle status, source, date checked, available quantity, required quantity including assembly allowance, and price at the relevant quantity. Include supplier part codes and assembly service restrictions where applicable. Consolidate identical parts into one line.

Treat lifecycle status, distributor stock, and the assembler's usable inventory as separate facts. Avoid obsolete or not-recommended-for-new-design parts for new designs unless the user has a specific reason to retain them. Resolve conflicting lifecycle reports using manufacturer evidence; record unresolved uncertainty. Recheck availability before quotation or release because an earlier stock check is not a reservation.

Check the intended assembler's catalogue and service eligibility when one is selected. A part available through a distributor may still need sourcing or pre-order before the assembler can use it. For example, [JLCPCB documents separate warehouse and pre-order paths](https://jlcpcb.com/help/article/what-is-jlcpcb-parts-pre-order-service). Consult current supplier terms for lead times, minimum quantities, attrition allowances, and handling fees.

Do not silently substitute an automatically matched component. Compare the exact part's electrical, mechanical, and assembly requirements, then propagate the accepted change through the design. A package-compatible replacement can still change firmware or operating limits.

## Establish a cost baseline

Start with a manufacturer's suitable standard stack and fabrication capabilities. Compare total assembled cost at the requested quantity, including fabrication, components, setup, assembly operations, special package handling, sourcing, shipping, and applicable taxes. Mark unknown costs as unknown.

Check the cost implications of custom stacks, controlled-impedance services, small drills, special vias, finishes, fine-pitch packages, assembly sides, through-hole work, rails, and panelisation before finalising geometry. These are candidates to investigate, not universal surcharges. Do not choose a cheaper construction that fails the circuit or assembly requirements. Record the reason for expensive options that remain necessary.

Evaluate changes against both savings and engineering consequences. Recalculate routing geometry if the stack changes. Recheck thermal and soldering requirements if drills, vias, pads, or finish change. Prefer a suitable economical part at initial selection over redesigning a completed board for a small unit-price saving.

## Prepare and compare quotations

Prepare the supplier's requested bundle from a single identified revision. It may include fabrication files, BOM, placement data, assembly drawings, and notes explaining intentional overhangs, acoustic openings, unusual footprints, or assembly requirements. Use the CAD skill for export and file consistency checks. Mark preliminary packages and unresolved findings clearly.

Keep the revision, complete manufacturing settings, quantity, currency, delivery destination, quote date, and supplier quote reference together with the price evidence. Changing one calculator option can reset another: reread all price-relevant settings after changes and before reporting savings. Compare equivalent specifications, or explain the differences explicitly.

Distinguish an estimate, a calculator subtotal, a submitted sourcing request, and a reviewed complete quote. List included and excluded costs, promotions, stock shortages, and pending supplier review. Do not carry an earlier revision's price forward as a fresh quote. Inspect component matching and placement previews where the supplier provides them.

Prepare the complete relevant bundle before requesting upload permission if required by the active tools or approval system. Reuse existing authorisation within its scope. A quotation task does not authorise purchases, paid matching services, or accepting declarations beyond the user's authorisation. Stop at an actual login, approval, or supplier-review dependency and state what remains pending.
