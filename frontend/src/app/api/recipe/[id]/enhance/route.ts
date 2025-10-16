import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET(
  _req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = await params;
    const res = await fetch(`${BACKEND_URL}/recipe/${id}/enhance`, {
      method: "GET",
    });
    if (!res.ok) {
      const msg = await res.json().catch(() => ({ message: "Error" }));
      return NextResponse.json(msg, { status: res.status });
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { message: "Backend unreachable" },
      { status: 502 }
    );
  }
}
