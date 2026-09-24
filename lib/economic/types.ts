export type EconomicEntryType =
  | "ASSET"
  | "RESOURCE"
  | "IP"
  | "REVENUE"
  | "RECEIVABLE"
  | "CRYPTO"
  | "FIAT"
  | "EXPENSE"
  | "LIABILITY"
  | "OPPORTUNITY"
  | "UNKNOWN";

export type ValuationStatus = "VERIFIED" | "SUPPORTED" | "ESTIMATED" | "UNKNOWN";

export interface EconomicEntry {
  id: string;
  type: EconomicEntryType;
  owner: string;
  description: string;
  quantity?: number;
  unit?: string;
  currency?: string;
  costBasis?: number;
  realizedValue?: number;
  estimatedValue?: number;
  valuationStatus?: ValuationStatus;
  valuationMethod?: string;
  evidenceRefs: string[];
  acquisitionEvent?: string;
  liabilityRefs?: string[];
  lastVerified?: string;
  source?: string;
}

export interface EconomicSummary {
  realizedCash: number;
  verifiedReceivables: number;
  verifiedLiquidAssets: number;
  verifiedControlledResources: number;
  verifiedLiabilities: number;
  realizedEconomicPosition: number;
  estimatedOpportunityValue: number;
  unpricedEntries: number;
  byType: Record<EconomicEntryType, number>;
}
