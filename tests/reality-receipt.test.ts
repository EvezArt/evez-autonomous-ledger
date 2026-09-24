import assert from "node:assert/strict";
import { projectRealityReceipt } from "@/lib/economic/reality-receipt";
import type { RealityGateReceipt } from "@/lib/economic/reality-receipt-types";

const base: RealityGateReceipt = {
  envelopeHash: "env-123",
  actor: "EVEZ",
  target: "stripe:test",
  requestedEffect: "record revenue",
  authority: "HUMAN",
  evidenceRefs: ["payment:123"],
  policyVersion: "reality-1",
  decision: "ALLOW",
  drift: 0,
  executionStatus: "COMPLETED",
  spineSequence: 42,
  requestedValue: 25,
  currency: "USD",
  economicType: "REVENUE",
  declaredEffect: "record revenue",
  effectiveEffect: "record revenue",
};

const accepted = projectRealityReceipt(base);
assert.equal(accepted.accepted, true);
assert.equal(accepted.entry?.realizedValue, 25);
assert.deepEqual(accepted.entry?.evidenceRefs, ["payment:123", "env-123", "spine:42"]);
assert.equal(projectRealityReceipt({...base, decision:"BLOCK"}).reason, "NOT_ALLOWED");
assert.equal(projectRealityReceipt({...base, executionStatus:"FAILED"}).reason, "NOT_COMPLETED");
assert.equal(projectRealityReceipt({...base, evidenceRefs:[]}).reason, "MISSING_EVIDENCE");
assert.equal(projectRealityReceipt({...base, requestedValue:undefined}).reason, "MISSING_VALUE");
assert.equal(projectRealityReceipt({...base, declaredEffect:"x", effectiveEffect:"y"}).reason, "DECLARED_EFFECT_MISMATCH");
