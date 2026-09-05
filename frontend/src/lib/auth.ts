import Cookies from "js-cookie";

// JWT is stored in a cookie so Next.js middleware can read it for route protection.
const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export function setTokens(accessToken: string, refreshToken: string) {
  Cookies.set(ACCESS_TOKEN_KEY, accessToken, { sameSite: "lax", expires: 7 });
  Cookies.set(REFRESH_TOKEN_KEY, refreshToken, { sameSite: "lax", expires: 7 });
}

export function getAccessToken(): string | undefined {
  return Cookies.get(ACCESS_TOKEN_KEY);
}

export function clearTokens() {
  Cookies.remove(ACCESS_TOKEN_KEY);
  Cookies.remove(REFRESH_TOKEN_KEY);
}
