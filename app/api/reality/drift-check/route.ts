import { NextResponse } from "next/server";
import { checkRealityDrift } from "@/lib/economic/drift-guard";
import type { DriftCheckInput } from "@/lib/economic/drift-types";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as DriftCheckInput;
    const result = checkRealityDrift(body);
    return NextResponse.json(result, { status: result.status === "CLEAN" ? 200 : 409 });
  } catch (error) {
    return NextResponse.json(
      { error: "invalid JSON request", detail: error instanceof Error ? error.message : String(error) },
      { status: 400 }
    );
  }
}
