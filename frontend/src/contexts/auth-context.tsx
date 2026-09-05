"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { setTokens, clearTokens, getAccessToken } from "@/lib/auth";
import { User, AuthTokens } from "@/types";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Restore the session on first load if a token is present.
  useEffect(() => {
    async function loadUser() {
      if (!getAccessToken()) {
        setLoading(false);
        return;
      }
      try {
        const { data } = await api.get<User>("/auth/me");
        setUser(data);
      } catch {
        clearTokens();
      } finally {
        setLoading(false);
      }
    }
    loadUser();
  }, []);

  async function login(email: string, password: string) {
    const { data } = await api.post<AuthTokens>("/auth/login", { email, password });
    setTokens(data.access_token, data.refresh_token);
    const me = await api.get<User>("/auth/me");
    setUser(me.data);
    router.push("/dashboard");
  }

  async function register(name: string, email: string, password: string) {
    await api.post("/auth/register", { name, email, password });
    await login(email, password);
  }

  function logout() {
    clearTokens();
    setUser(null);
    router.push("/login");
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
