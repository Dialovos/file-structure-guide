package com.example.api;

import com.example.core.CoreUtils;

/**
 * Thin client over {@link CoreUtils}. Real projects would talk to an
 * external service here; this stub just demonstrates that {@code :api}
 * depends on {@code :core} and re-exports a portion of its surface.
 */
public final class ApiClient {

  /** Greets a user via core utilities. */
  public String greet(String name) {
    return CoreUtils.greet(name);
  }
}
