import { checkRealityDrift } from "@/lib/economic/drift-guard";
import type { DriftCheckInput } from "@/lib/economic/drift-types";

const base: DriftCheckInput = {
  actor: "EVEZ",
  projectIdentity: "EVEZ",
  subject: "ledger",
  statement: "The receipt exists.",
  claimClass: "OBSERVATION",
  evidenceRefs: ["receipt-1"],
  eventRefs: ["event-1"],
  reproducible: true,
};

const assert = (condition: boolean, message: string) => {
  if (!condition) throw new Error(message);
};

const clean = checkRealityDrift(base);
assert(clean.status === "CLEAN", "supported observation should be clean");

const unsupported = checkRealityDrift({
  ...base,
  claimClass: "VERIFIED_FACT",
  evidenceRefs: [],
  eventRefs: [],
});
assert(unsupported.status === "EVIDENCE_REQUIRED", "verified fact without evidence must be gated");

const narrative = checkRealityDrift({
  ...base,
  claimClass: "NARRATIVE",
  narrativeLanguage: true,
  externalEffectRequested: true,
});
assert(narrative.externalEffectAllowed === false, "narrative cannot authorize external effects");

console.log("reality drift guard checks passed");
