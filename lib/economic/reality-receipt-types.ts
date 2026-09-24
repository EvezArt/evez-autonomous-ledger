import type { EconomicEntry } from "./types";

export type RealityDecision = "ALLOW" | "BLOCK" | "CONTAIN" | "WITNESS_REQUIRED";
export type ExecutionStatus = "NOT_EXECUTED" | "COMPLETED" | "FAILED";

export interface RealityGateReceipt {
  envelopeHash: string;
  actor: string;
  target: string;
  requestedEffect: string;
  authority: string;
  evidenceRefs: string[];
  policyVersion: string;
  decision: RealityDecision;
  drift: number;
  executionStatus: ExecutionStatus;
  spineSequence: number;
  requestedValue?: number;
  currency?: string;
  economicType?: EconomicEntry["type"];
  declaredEffect?: string;
  effectiveEffect?: string;
}

export interface EconomicReceiptProjection {
  accepted: boolean;
  reason:
    | "COMPLETED_ALLOWED_EFFECT"
    | "NOT_ALLOWED"
    | "NOT_COMPLETED"
    | "MISSING_EVIDENCE"
    | "MISSING_VALUE"
    | "INVALID_VALUE"
    | "DECLARED_EFFECT_MISMATCH";
  entry?: EconomicEntry;
}
