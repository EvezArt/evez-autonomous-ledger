import { NextResponse } from "next/server";
import { summarizeEconomicEntries, validateEconomicEntry } from "@/lib/economic/ledger";
import type { EconomicEntry } from "@/lib/economic/types";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as { entries?: EconomicEntry[] };
    if (!Array.isArray(body.entries)) {
      return NextResponse.json({ error: "entries must be an array" }, { status: 400 });
    }

    const errors = body.entries.flatMap((entry, index) =>
      validateEconomicEntry(entry).map((error) => ({ index, error }))
    );

    if (errors.length > 0) {
      return NextResponse.json({ error: "invalid entries", details: errors }, { status: 422 });
    }

    return NextResponse.json({
      summary: summarizeEconomicEntries(body.entries),
      entryCount: body.entries.length,
      invariant: "CLAIMED VALUE != REALIZED VALUE",
    });
  } catch (error) {
    return NextResponse.json(
      { error: "invalid JSON request", detail: error instanceof Error ? error.message : String(error) },
      { status: 400 }
    );
  }
}
