package com.example.myproject;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class AppTest {

  @Test
  void greetReturnsGreeting() {
    assertEquals("hello, alice", new App().greet("alice"));
  }

  @Test
  void greetRejectsBlankName() {
    assertThrows(IllegalArgumentException.class, () -> new App().greet(""));
  }
}
