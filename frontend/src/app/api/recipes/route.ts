import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND_URL}/`, { cache: "no-store" });
    if (!res.ok) {
      return NextResponse.json(
        { message: "Failed to fetch recipes" },
        { status: res.status }
      );
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
