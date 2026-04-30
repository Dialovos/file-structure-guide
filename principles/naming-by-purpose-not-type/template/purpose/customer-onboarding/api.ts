// purpose/customer-onboarding/api.ts
// The HTTP client for customer onboarding lives next to the form that calls
// it and the types they share. Moving onboarding to another module is one
// `git mv` of this directory, not three.

import type { OnboardingDraft, OnboardingResult } from "./types";

export async function startOnboarding(
  draft: OnboardingDraft,
): Promise<OnboardingResult> {
  const res = await fetch("/api/onboarding", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(draft),
  });
  if (!res.ok) throw new Error(`onboarding failed: ${res.status}`);
  return res.json();
}
