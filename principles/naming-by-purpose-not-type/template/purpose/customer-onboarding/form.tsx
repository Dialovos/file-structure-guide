// purpose/customer-onboarding/form.tsx
// The form component for customer onboarding lives next to its API client
// and its shared types — one purpose, one directory.

import { startOnboarding } from "./api";
import type { OnboardingDraft } from "./types";

export function CustomerOnboardingForm() {
  const onSubmit = async (draft: OnboardingDraft) => {
    await startOnboarding(draft);
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); /* gather + submit */ }}>
      <input name="email" type="email" required />
      <button type="submit">Start onboarding</button>
    </form>
  );
}
