import assert from "node:assert/strict";
import { checkRealityDrift } from "@/lib/economic/drift-guard";
import type { DriftCheckInput } from "@/lib/economic/drift-types";

const base: DriftCheckInput = {
  actor: "EVEZ", projectIdentity: "EVEZ", subject: "ledger",
  statement: "The receipt exists.", claimClass: "OBSERVATION",
  evidenceRefs: ["receipt-1"], eventRefs: ["event-1"], reproducible: true,
};

const clean = checkRealityDrift(base);
assert.equal(clean.status, "CLEAN");

const unsupported = checkRealityDrift({
  ...base, claimClass: "VERIFIED_FACT", evidenceRefs: [], eventRefs: [],
});
assert.equal(unsupported.status, "EVIDENCE_REQUIRED");

const narrative = checkRealityDrift({
  ...base, claimClass: "NARRATIVE", narrativeLanguage: true,
  externalEffectRequested: true,
});
assert.equal(narrative.externalEffectAllowed, false);

console.log("reality drift guard checks passed");
