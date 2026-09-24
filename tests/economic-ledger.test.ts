import assert from "node:assert/strict";
import { summarizeEconomicEntries, validateEconomicEntry } from "@/lib/economic/ledger";
import type { EconomicEntry } from "@/lib/economic/types";

const entry = (patch: Partial<EconomicEntry>): EconomicEntry => ({
  id: "x", type: "ASSET", owner: "EVEZ", description: "test",
  evidenceRefs: ["evt-1"], valuationStatus: "VERIFIED", ...patch,
});

const opportunity = summarizeEconomicEntries([
  entry({ id: "cash", type: "FIAT", realizedValue: 125 }),
  entry({ id: "opp", type: "OPPORTUNITY", estimatedValue: 1000000, valuationStatus: "ESTIMATED" }),
]);
assert.equal(opportunity.realizedCash, 125);
assert.equal(opportunity.estimatedOpportunityValue, 1000000);
assert.equal(opportunity.realizedEconomicPosition, 125);

const flow = summarizeEconomicEntries([
  entry({ id: "cash", type: "FIAT", realizedValue: 125 }),
  entry({ id: "sale", type: "REVENUE", realizedValue: 50 }),
]);
assert.equal(flow.realizedEconomicPosition, 125);
assert.equal(flow.netCashFlow, 50);

const liabilities = summarizeEconomicEntries([
  entry({ id: "cash", type: "FIAT", realizedValue: 1000 }),
  entry({ id: "crypto", type: "CRYPTO", realizedValue: 400 }),
  entry({ id: "debt", type: "LIABILITY", realizedValue: 300 }),
]);
assert.equal(liabilities.realizedEconomicPosition, 1100);

const unproven = summarizeEconomicEntries([
  entry({ id: "unproven", type: "ASSET", estimatedValue: 5000, evidenceRefs: [] }),
]);
assert.equal(unproven.verifiedControlledResources, 0);

const errors = validateEconomicEntry(entry({ id: "", description: "" }));
assert(errors.includes("id is required"));
assert(errors.includes("description is required"));
