package com.example.app;

import com.example.api.ApiClient;

/**
 * Application entry point. Demonstrates the dependency chain
 * {@code :app} → {@code :api} → {@code :core}.
 */
public final class App {

  public static void main(String[] args) {
    String who = args.length > 0 ? args[0] : "world";
    System.out.println(new ApiClient().greet(who));
  }
}
