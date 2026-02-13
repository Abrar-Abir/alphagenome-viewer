import { createContext, useContext, useEffect, useState } from "react"

const ThemeContext = createContext({ theme: "system", setTheme: () => {} })

const STORAGE_KEY = "theme"

function getSystemTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light"
}

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored === "light" || stored === "dark" ? stored : "system"
  })

  useEffect(() => {
    const root = document.documentElement
    const resolved = theme === "system" ? getSystemTheme() : theme

    root.classList.remove("light", "dark")
    root.classList.add(resolved)

    if (theme === "system") {
      localStorage.removeItem(STORAGE_KEY)
    } else {
      localStorage.setItem(STORAGE_KEY, theme)
    }
  }, [theme])

  useEffect(() => {
    if (theme !== "system") return

    const mql = window.matchMedia("(prefers-color-scheme: dark)")
    const handler = (e) => {
      const root = document.documentElement
      root.classList.remove("light", "dark")
      root.classList.add(e.matches ? "dark" : "light")
    }

    mql.addEventListener("change", handler)
    return () => mql.removeEventListener("change", handler)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}
