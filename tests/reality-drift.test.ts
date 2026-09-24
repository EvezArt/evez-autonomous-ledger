import assert from "node:assert/strict";
import { checkRealityDrift } from "@/lib/economic/drift-guard";
import type { DriftCheckInput } from "@/lib/economic/drift-types";

const base: DriftCheckInput = {
  actor: "EVEZ", projectIdentity: "EVEZ", subject: "ledger",
  statement: "The receipt exists.", claimClass: "OBSERVATION",
  evidenceRefs: ["receipt-1"], eventRefs: ["event-1"], reproducible: true,
};

assert.equal(checkRealityDrift(base).status, "CLEAN");
assert.equal(checkRealityDrift({...base, claimClass:"VERIFIED_FACT", evidenceRefs:[], eventRefs:[]}).status, "EVIDENCE_REQUIRED");
assert.equal(checkRealityDrift({...base, claimClass:"NARRATIVE", narrativeLanguage:true, externalEffectRequested:true}).externalEffectAllowed, false);
