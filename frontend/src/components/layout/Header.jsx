import { Sun, Moon, KeyRound } from "lucide-react";
import { useTheme } from "@/components/ThemeProvider";

export function Header({ onChangeApiKey }) {
	const { theme, setTheme } = useTheme();

	const toggleTheme = () => {
		if (theme === "system") {
			const isCurrentlyDark = document.documentElement.classList.contains("dark");
			setTheme(isCurrentlyDark ? "light" : "dark");
		} else if (theme === "dark") {
			setTheme("light");
		} else {
			setTheme("dark");
		}
	};

	const isDark =
		theme === "dark" ||
		(theme === "system" &&
			typeof window !== "undefined" &&
			window.matchMedia("(prefers-color-scheme: dark)").matches);

	return (
		<header className="bg-gradient-to-r from-sky-500 via-violet-500 to-pink-500 dark:from-sky-700 dark:via-violet-700 dark:to-pink-700 px-6 py-4">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-xl font-semibold text-white">AlphaGenome Viewer</h1>
					<p className="text-sm text-white/80">
						Genomic predictions powered by AlphaGenome
					</p>
				</div>
				<div className="flex items-center gap-1">
					<button
						onClick={onChangeApiKey}
						className="rounded-md p-2 text-white/80 hover:text-white hover:bg-white/10 transition-colors"
						aria-label="Change API key"
						title="Change API key"
					>
						<KeyRound className="h-5 w-5" />
					</button>
					<button
						onClick={toggleTheme}
						className="rounded-md p-2 text-white/80 hover:text-white hover:bg-white/10 transition-colors"
						aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
						title={isDark ? "Switch to light mode" : "Switch to dark mode"}
					>
						{isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
					</button>
				</div>
			</div>
		</header>
	);
}
