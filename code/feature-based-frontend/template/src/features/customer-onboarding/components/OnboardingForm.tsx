import type { FC } from "react";

import type { OnboardingState } from "@/features/customer-onboarding/types";

export interface OnboardingFormProps {
  state: OnboardingState;
  onSubmit: (state: OnboardingState) => void;
}

/**
 * Multi-step onboarding form. Owns no global state; the parent
 * passes the current `state` and an `onSubmit` callback.
 */
export const OnboardingForm: FC<OnboardingFormProps> = ({ state, onSubmit }) => {
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(state);
      }}
    >
      <h2>Welcome, {state.email}</h2>
      <button type="submit">Continue</button>
    </form>
  );
};
