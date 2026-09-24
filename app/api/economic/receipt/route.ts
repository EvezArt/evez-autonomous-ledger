import { NextResponse } from "next/server";
import { projectRealityReceipt } from "@/lib/economic/reality-receipt";
import type { RealityGateReceipt } from "@/lib/economic/reality-receipt-types";

export async function POST(request: Request) {
  try {
    const receipt = (await request.json()) as RealityGateReceipt;
    const result = projectRealityReceipt(receipt);
    return NextResponse.json(result, { status: result.accepted ? 200 : 422 });
  } catch (error) {
    return NextResponse.json(
      { error: "invalid JSON request", detail: error instanceof Error ? error.message : String(error) },
      { status: 400 }
    );
  }
}
