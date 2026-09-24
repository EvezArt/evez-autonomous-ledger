import type { EconomicEntry, EconomicSummary, EconomicEntryType } from "./types";

const VERIFIED_VALUE = new Set(["VERIFIED", "SUPPORTED"]);
const CONTROLLED_VALUE_TYPES = new Set<EconomicEntryType>(["ASSET", "RESOURCE", "IP"]);

function numeric(value: number | undefined): number {
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

function valueOf(entry: EconomicEntry): number {
  const realized = numeric(entry.realizedValue);
  return realized !== 0 ? realized : numeric(entry.estimatedValue);
}

function verified(entry: EconomicEntry): boolean {
  return VERIFIED_VALUE.has(entry.valuationStatus ?? "UNKNOWN") && entry.evidenceRefs.length > 0;
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
  const types: EconomicEntryType[] = [
    "ASSET", "RESOURCE", "IP", "REVENUE", "RECEIVABLE", "CRYPTO",
    "FIAT", "EXPENSE", "LIABILITY", "OPPORTUNITY", "UNKNOWN"
  ];
  const byType = Object.fromEntries(types.map((type) => [type, 0])) as Record<EconomicEntryType, number>;

  let realizedCash = 0;
  let realizedRevenue = 0;
  let realizedExpenses = 0;
  let verifiedReceivables = 0;
  let verifiedLiquidAssets = 0;
  let verifiedControlledResources = 0;
  let verifiedLiabilities = 0;
  let estimatedOpportunityValue = 0;
  let unpricedEntries = 0;

  for (const entry of entries) {
    const value = valueOf(entry);
    byType[entry.type] += value;

    const isVerified = verified(entry);

    if (entry.type === "FIAT" && isVerified) realizedCash += numeric(entry.realizedValue);
    if (entry.type === "REVENUE" && isVerified) realizedRevenue += numeric(entry.realizedValue);
    if (entry.type === "EXPENSE" && isVerified) realizedExpenses += numeric(entry.realizedValue);
    if (entry.type === "CRYPTO" && isVerified) verifiedLiquidAssets += numeric(entry.realizedValue);
    if (entry.type === "RECEIVABLE" && isVerified) verifiedReceivables += value;
    if (entry.type === "LIABILITY" && isVerified) verifiedLiabilities += value;
    if (CONTROLLED_VALUE_TYPES.has(entry.type) && isVerified) verifiedControlledResources += value;
    if (entry.type === "OPPORTUNITY") estimatedOpportunityValue += numeric(entry.estimatedValue);
    if (value === 0 && entry.type !== "UNKNOWN") unpricedEntries += 1;
  }

  const netCashFlow = realizedRevenue - realizedExpenses;
  const realizedEconomicPosition =
    realizedCash +
    verifiedLiquidAssets +
    verifiedReceivables +
    verifiedControlledResources -
    verifiedLiabilities;

  return {
    realizedCash,
    realizedRevenue,
    realizedExpenses,
    netCashFlow,
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
    throw new Error("economic position is negative; inspect verified liabilities and asset evidence");
  }
}
