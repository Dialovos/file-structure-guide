import type { OnboardingState } from "@/features/customer-onboarding/types";

const ONBOARDING_ENDPOINT = "/api/onboarding";

/**
 * Submit the completed onboarding state to the backend.
 *
 * No React, no JSX in this file — only the network layer for the
 * customer-onboarding feature lives here.
 */
export async function submitOnboarding(state: OnboardingState): Promise<void> {
  const response = await fetch(ONBOARDING_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state),
  });
  if (!response.ok) {
    throw new Error(`onboarding submission failed: ${response.status}`);
  }
}

/** Fetch the latest onboarding state for the current user. */
export async function fetchOnboarding(): Promise<OnboardingState | null> {
  const response = await fetch(ONBOARDING_ENDPOINT);
  if (response.status === 404) return null;
  if (!response.ok) {
    throw new Error(`onboarding fetch failed: ${response.status}`);
  }
  return (await response.json()) as OnboardingState;
}
