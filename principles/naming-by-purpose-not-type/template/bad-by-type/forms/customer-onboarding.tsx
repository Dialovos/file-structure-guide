// bad-by-type/forms/customer-onboarding.tsx
//
// ANTI-PATTERN — DO NOT COPY THIS LAYOUT.
//
// This file lives in `forms/` because it is "a form". Its API client lives
// in `api/onboarding.ts`. Its types live in `types/onboarding.ts`. To make
// any meaningful change to customer onboarding you must open three sibling
// directories and keep three filename conventions in sync (is it
// `customer-onboarding.tsx` here, but `onboarding.ts` over there? Already a
// drift waiting to bite).
//
// The fix: collapse all three files into a single purpose dir,
// `customer-onboarding/`, with `form.tsx`, `api.ts`, and `types.ts` as
// peers inside it. See `../purpose/customer-onboarding/` for the good shape.

export function CustomerOnboardingForm() {
  // Imagine this imports from "../api/onboarding" and "../types/onboarding".
  // Three sibling directories for one feature.
  return <form>onboarding</form>;
}
