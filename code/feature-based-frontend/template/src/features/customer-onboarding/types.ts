/** Public types for the customer-onboarding feature. */

export interface OnboardingState {
  email: string;
  /** Zero-based step index. */
  step: number;
}

export type OnboardingStep =
  | "email"
  | "profile"
  | "preferences"
  | "review";
