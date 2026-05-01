package com.example.core;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class CoreUtilsTest {

  @Test
  void greetReturnsGreeting() {
    assertEquals("hello, alice", CoreUtils.greet("alice"));
  }

  @Test
  void greetRejectsBlankName() {
    assertThrows(IllegalArgumentException.class, () -> CoreUtils.greet(""));
  }
}
