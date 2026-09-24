import type { EconomicEntry, EconomicSummary, EconomicEntryType } from "./types";

const LIABILITY_TYPES = new Set<EconomicEntryType>(["LIABILITY", "EXPENSE"]);
const LIQUID_TYPES = new Set<EconomicEntryType>(["FIAT", "CRYPTO"]);
const VERIFIED_VALUE = new Set(["VERIFIED", "SUPPORTED"]);

function numeric(value: number | undefined): number {
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

function valueOf(entry: EconomicEntry): number {
  const realized = numeric(entry.realizedValue);
  if (realized !== 0) return realized;
  return numeric(entry.estimatedValue);
}

export function validateEconomicEntry(entry: EconomicEntry): string[] {
  const errors: string[] = [];
  if (!entry.id.trim()) errors.push("id is required");
  if (!entry.owner.trim()) errors.push("owner is required");
  if (!entry.description.trim()) errors.push("description is required");
  if (!entry.type) errors.push("type is required");
  if (!Array.isArray(entry.evidenceRefs)) errors.push("evidenceRefs must be an array");
  if (entry.quantity !== undefined && !Number.isFinite(entry.quantity)) errors.push("quantity must be finite");
  if (entry.currency && entry.currency.length > 16) errors.push("currency is too long");
  return errors;
}

export function summarizeEconomicEntries(entries: EconomicEntry[]): EconomicSummary {
  const byType = Object.fromEntries(
    (["ASSET","RESOURCE","IP","REVENUE","RECEIVABLE","CRYPTO","FIAT","EXPENSE","LIABILITY","OPPORTUNITY","UNKNOWN"] as EconomicEntryType[])
      .map((type) => [type, 0])
  ) as Record<EconomicEntryType, number>;

  let realizedCash = 0;
  let verifiedReceivables = 0;
  let verifiedLiquidAssets = 0;
  let verifiedControlledResources = 0;
  let verifiedLiabilities = 0;
  let estimatedOpportunityValue = 0;
  let unpricedEntries = 0;

  for (const entry of entries) {
    const value = valueOf(entry);
    byType[entry.type] += value;

    const verified = VERIFIED_VALUE.has(entry.valuationStatus ?? "UNKNOWN") && entry.evidenceRefs.length > 0;

    if (entry.type === "FIAT" && verified) realizedCash += numeric(entry.realizedValue);
    if (entry.type === "REVENUE" && verified) realizedCash += numeric(entry.realizedValue);
    if (entry.type === "RECEIVABLE" && verified) verifiedReceivables += value;
    if (LIQUID_TYPES.has(entry.type) && verified) verifiedLiquidAssets += value;
    if ((entry.type === "ASSET" || entry.type === "RESOURCE" || entry.type === "IP") && verified) {
      verifiedControlledResources += value;
    }
    if (LIABILITY_TYPES.has(entry.type) && verified) verifiedLiabilities += value;
    if (entry.type === "OPPORTUNITY") estimatedOpportunityValue += numeric(entry.estimatedValue);
    if (value === 0 && entry.type !== "UNKNOWN") unpricedEntries += 1;
  }

  const realizedEconomicPosition =
    realizedCash +
    verifiedReceivables +
    verifiedLiquidAssets +
    verifiedControlledResources -
    verifiedLiabilities;

  return {
    realizedCash,
    verifiedReceivables,
    verifiedLiquidAssets,
    verifiedControlledResources,
    verifiedLiabilities,
    realizedEconomicPosition,
    estimatedOpportunityValue,
    unpricedEntries,
    byType,
  };
}

export function assertNoFakeValue(summary: EconomicSummary): void {
  if (summary.realizedEconomicPosition < -1e-9) {
    throw new Error("economic position cannot be represented as negative without an explicit liability policy");
  }
}
