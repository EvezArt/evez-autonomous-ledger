import type { DriftCheckInput, DriftCheckResult } from "./drift-types";

const BLOCKING_CLASSES = new Set(["HYPOTHESIS", "FICTION", "NARRATIVE", "UNKNOWN"]);
const CLAIMS_REQUIRING_EVIDENCE = new Set(["VERIFIED_FACT", "SUPPORTED_INFERENCE"]);

export function checkRealityDrift(input: DriftCheckInput): DriftCheckResult {
  const reasons: string[] = [];
  const hasEvidence = input.evidenceRefs.length > 0 || input.eventRefs.length > 0;

  if (!input.statement.trim()) reasons.push("EMPTY_STATEMENT");
  if (!input.actor.trim()) reasons.push("MISSING_ACTOR");
  if (!input.subject.trim()) reasons.push("MISSING_SUBJECT");

  if (CLAIMS_REQUIRING_EVIDENCE.has(input.claimClass) && !hasEvidence) {
    reasons.push("MISSING_EVIDENCE");
  }

  if (input.claimClass === "SUPPORTED_INFERENCE" && !input.reproducible) {
    reasons.push("UNREPRODUCIBLE");
  }

  if (input.narrativeLanguage && input.claimClass !== "FICTION" && input.claimClass !== "NARRATIVE") {
    reasons.push("NARRATIVE_TREATED_AS_FACT");
  }

  if (input.externalEffectRequested && BLOCKING_CLASSES.has(input.claimClass)) {
    reasons.push("EXTERNAL_ACTION_FROM_UNCERTAINTY");
  }

  const identityConfusion =
    input.subject.toLowerCase().includes("evez") &&
    input.statement.toLowerCase().includes("steven") &&
    input.claimClass !== "OBSERVATION" &&
    input.claimClass !== "VERIFIED_FACT";

  if (identityConfusion) reasons.push("IDENTITY_CONFUSION");

  const blocking = input.externalEffectRequested
    ? reasons.length > 0 || BLOCKING_CLASSES.has(input.claimClass)
    : reasons.length > 0;

  const status: DriftCheckResult["status"] =
    reasons.length === 0
      ? "CLEAN"
      : input.claimClass === "UNKNOWN" || !hasEvidence
        ? "EVIDENCE_REQUIRED"
        : "DRIFT_DETECTED";

  return {
    status,
    correction:
      status === "CLEAN"
        ? "Claim is bounded by its declared class and available evidence."
        : [
            "DRIFT DETECTED",
            "Claim exceeds evidence.",
            "Return to observable state.",
            "What happened?",
            "What changed?",
            "What is recorded?",
            "What remains unknown?",
            "What can be reproduced?",
          ].join("\n"),
    reasonCodes: reasons,
    claimClass: input.claimClass,
    evidenceRefs: input.evidenceRefs,
    eventRefs: input.eventRefs,
    externalEffectAllowed: !blocking,
  };
}
