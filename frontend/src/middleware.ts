import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const { pathname } = request.nextUrl;
  const isPublic = PUBLIC_PATHS.some((p) => pathname.startsWith(p));

  // Not logged in and visiting a protected page -> go to login.
  if (!token && !isPublic) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  // Already logged in and visiting login/register -> go to dashboard.
  if (token && isPublic) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }
  return NextResponse.next();
}

export const config = {
  // Run on everything except Next internals and static files.
  matcher: ["/((?!api|_next|.*\\..*).*)"],
};
