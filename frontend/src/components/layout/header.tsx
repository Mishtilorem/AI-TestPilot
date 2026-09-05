"use client";

import { useTheme } from "next-themes";
import { Moon, Sun, LogOut } from "lucide-react";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";

export function Header() {
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();

  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="text-sm text-muted-foreground">
        {user ? `Signed in as ${user.name}` : ""}
      </div>
      <div className="flex items-center gap-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          aria-label="Toggle theme"
        >
          <Sun className="h-5 w-5 dark:hidden" />
          <Moon className="hidden h-5 w-5 dark:block" />
        </Button>
        <Button variant="ghost" size="icon" onClick={logout} aria-label="Log out">
          <LogOut className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
}
