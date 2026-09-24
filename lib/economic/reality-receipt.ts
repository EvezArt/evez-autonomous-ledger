import type { EconomicEntry } from "./types";
import type { EconomicReceiptProjection, RealityGateReceipt } from "./reality-receipt-types";

const VALUE_TYPES = new Set<EconomicEntry["type"]>([
  "FIAT", "CRYPTO", "RECEIVABLE", "ASSET", "RESOURCE", "IP", "REVENUE", "EXPENSE", "LIABILITY"
]);

function validAmount(value: number | undefined): value is number {
  return typeof value === "number" && Number.isFinite(value) && value >= 0;
}

export function projectRealityReceipt(receipt: RealityGateReceipt): EconomicReceiptProjection {
  if (receipt.decision !== "ALLOW") return { accepted: false, reason: "NOT_ALLOWED" };
  if (receipt.executionStatus !== "COMPLETED") return { accepted: false, reason: "NOT_COMPLETED" };
  if (receipt.evidenceRefs.length === 0) return { accepted: false, reason: "MISSING_EVIDENCE" };
  if (receipt.declaredEffect && receipt.effectiveEffect && receipt.declaredEffect !== receipt.effectiveEffect) {
    return { accepted: false, reason: "DECLARED_EFFECT_MISMATCH" };
  }

  const type = receipt.economicType;
  if (!type || !VALUE_TYPES.has(type)) return { accepted: false, reason: "MISSING_VALUE" };
  if (!validAmount(receipt.requestedValue)) {
    return { accepted: false, reason: receipt.requestedValue === undefined ? "MISSING_VALUE" : "INVALID_VALUE" };
  }

  const entry: EconomicEntry = {
    id: receipt.envelopeHash,
    type,
    owner: receipt.actor,
    description: receipt.requestedEffect,
    realizedValue: receipt.requestedValue,
    currency: receipt.currency,
    valuationStatus: "VERIFIED",
    valuationMethod: "Reality Gate completed execution receipt",
    evidenceRefs: receipt.evidenceRefs.concat(
      receipt.envelopeHash,
      "spine:" + String(receipt.spineSequence)
    ),
    source: "evez-event-spine/reality-gate",
    lastVerified: new Date().toISOString(),
  };

  return { accepted: true, reason: "COMPLETED_ALLOWED_EFFECT", entry };
}
