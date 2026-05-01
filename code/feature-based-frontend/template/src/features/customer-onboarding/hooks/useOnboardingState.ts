import { useCallback, useEffect, useState } from "react";

import { fetchOnboarding } from "@/features/customer-onboarding/api/onboarding-client";
import type { OnboardingState } from "@/features/customer-onboarding/types";

const INITIAL_STATE: OnboardingState = {
  email: "",
  step: 0,
};

/**
 * Loads and tracks the onboarding state for the current user.
 * Encapsulates the React-side wiring so components can stay
 * presentational.
 */
export function useOnboardingState(): {
  state: OnboardingState;
  setState: (state: OnboardingState) => void;
  loading: boolean;
} {
  const [state, setStateInternal] = useState<OnboardingState>(INITIAL_STATE);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const remote = await fetchOnboarding();
      if (!cancelled && remote) {
        setStateInternal(remote);
      }
      if (!cancelled) {
        setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const setState = useCallback((next: OnboardingState) => {
    setStateInternal(next);
  }, []);

  return { state, setState, loading };
}
