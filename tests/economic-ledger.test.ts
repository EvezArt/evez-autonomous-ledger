import { describe, expect, it } from "vitest";
import { summarizeEconomicEntries, validateEconomicEntry } from "@/lib/economic/ledger";
import type { EconomicEntry } from "@/lib/economic/types";

const entry = (patch: Partial<EconomicEntry>): EconomicEntry => ({
  id: "x",
  type: "ASSET",
  owner: "EVEZ",
  description: "test",
  evidenceRefs: ["evt-1"],
  valuationStatus: "VERIFIED",
  ...patch,
});

describe("economic ledger", () => {
  it("separates position from opportunity value", () => {
    const s = summarizeEconomicEntries([
      entry({ id: "cash", type: "FIAT", realizedValue: 125 }),
      entry({ id: "opp", type: "OPPORTUNITY", estimatedValue: 1000000, valuationStatus: "ESTIMATED" }),
    ]);
    expect(s.realizedCash).toBe(125);
    expect(s.estimatedOpportunityValue).toBe(1000000);
    expect(s.realizedEconomicPosition).toBe(125);
  });

  it("does not treat revenue as additional cash balance", () => {
    const s = summarizeEconomicEntries([
      entry({ id: "cash", type: "FIAT", realizedValue: 125 }),
      entry({ id: "sale", type: "REVENUE", realizedValue: 50 }),
    ]);
    expect(s.realizedCash).toBe(125);
    expect(s.realizedRevenue).toBe(50);
    expect(s.realizedEconomicPosition).toBe(125);
    expect(s.netCashFlow).toBe(50);
  });

  it("tracks crypto and liabilities without double counting fiat", () => {
    const s = summarizeEconomicEntries([
      entry({ id: "cash", type: "FIAT", realizedValue: 1000 }),
      entry({ id: "crypto", type: "CRYPTO", realizedValue: 400 }),
      entry({ id: "debt", type: "LIABILITY", realizedValue: 300 }),
    ]);
    expect(s.verifiedLiquidAssets).toBe(400);
    expect(s.verifiedLiabilities).toBe(300);
    expect(s.realizedEconomicPosition).toBe(1100);
  });

  it("requires evidence before treating value as verified", () => {
    const s = summarizeEconomicEntries([
      entry({ id: "unproven", type: "ASSET", estimatedValue: 5000, evidenceRefs: [] }),
    ]);
    expect(s.verifiedControlledResources).toBe(0);
  });

  it("rejects malformed entries", () => {
    const errors = validateEconomicEntry(entry({ id: "", description: "" }));
    expect(errors).toContain("id is required");
    expect(errors).toContain("description is required");
  });
});
