/**
 * customer-onboarding — public API.
 *
 * Other features import from this barrel and only this barrel.
 * Internal modules (anything not re-exported here) are private to
 * the feature; refactor freely behind this seam.
 */

export { OnboardingForm } from "./components/OnboardingForm";
export type { OnboardingFormProps } from "./components/OnboardingForm";
export { ProgressIndicator } from "./components/ProgressIndicator";
export { useOnboardingState } from "./hooks/useOnboardingState";
export type { OnboardingState, OnboardingStep } from "./types";

// Network helpers stay internal — other features should not call
// the onboarding API directly. Expose a hook or a wrapper if a
// second consumer ever needs it.
