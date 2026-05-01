import type { FC } from "react";

export interface ProgressIndicatorProps {
  /** Zero-based index of the current step. */
  currentStep: number;
  /** Total number of steps. */
  totalSteps: number;
}

/**
 * Renders a "Step X of Y" indicator. Stateless; the consumer feeds
 * the current step in.
 */
export const ProgressIndicator: FC<ProgressIndicatorProps> = ({ currentStep, totalSteps }) => {
  return (
    <p aria-label="onboarding-progress">
      Step {currentStep + 1} of {totalSteps}
    </p>
  );
};
