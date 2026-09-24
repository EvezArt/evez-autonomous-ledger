export type DriftClaimClass =
  | "OBSERVATION"
  | "VERIFIED_FACT"
  | "SUPPORTED_INFERENCE"
  | "HYPOTHESIS"
  | "FICTION"
  | "NARRATIVE"
  | "UNKNOWN";

export type DriftStatus = "CLEAN" | "DRIFT_DETECTED" | "EVIDENCE_REQUIRED";

export interface DriftCheckInput {
  actor: string;
  projectIdentity: "EVEZ" | string;
  subject: string;
  statement: string;
  claimClass: DriftClaimClass;
  evidenceRefs: string[];
  eventRefs: string[];
  reproducible: boolean;
  externalEffectRequested?: boolean;
  narrativeLanguage?: boolean;
}

export interface DriftCheckResult {
  status: DriftStatus;
  correction: string;
  reasonCodes: string[];
  claimClass: DriftClaimClass;
  evidenceRefs: string[];
  eventRefs: string[];
  externalEffectAllowed: boolean;
}
