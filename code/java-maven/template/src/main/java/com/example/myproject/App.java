package com.example.myproject;

/**
 * Entry point for the myproject sample application.
 *
 * <p>This stub is intentionally tiny: it exists so that {@code mvn package}
 * has something to compile and tests have something to import. Replace
 * with real code as your application grows; move helpers into the
 * {@code core/} subpackage.
 */
public class App {

  /** Returns a friendly greeting. Used by {@code AppTest}. */
  public String greet(String name) {
    if (name == null || name.isBlank()) {
      throw new IllegalArgumentException("name must not be blank");
    }
    return "hello, " + name;
  }

  public static void main(String[] args) {
    String who = args.length > 0 ? args[0] : "world";
    System.out.println(new App().greet(who));
  }
}
