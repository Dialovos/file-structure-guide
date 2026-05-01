package com.example.core;

/**
 * Shared utilities used by every other module.
 *
 * <p>This stub exists so the build has something real to compile and so
 * downstream modules ({@code :api}, {@code :app}) have a non-trivial
 * dependency to call into.
 */
public final class CoreUtils {

  private CoreUtils() {}

  /** Returns a friendly greeting; never returns null. */
  public static String greet(String name) {
    if (name == null || name.isBlank()) {
      throw new IllegalArgumentException("name must not be blank");
    }
    return "hello, " + name;
  }
}
