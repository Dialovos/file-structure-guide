import { invoke } from "@tauri-apps/api/core";

// One typed wrapper per command; components never call invoke() with raw strings.
export const greet = (name: string) => invoke<string>("greet", { name });
