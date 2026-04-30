// purpose/customer-onboarding/types.ts
// Shared types for customer onboarding. Co-located with the only files that
// import them — no top-level `types/` dir to scatter them across.

export type OnboardingDraft = {
  email: string;
  companyName?: string;
};

export type OnboardingResult = {
  customerId: string;
  status: "active" | "pending";
};
