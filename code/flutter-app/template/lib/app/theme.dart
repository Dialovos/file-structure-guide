import 'package:flutter/material.dart';

/// App-wide [ThemeData]. Tweak the seed color or swap to a custom
/// `ColorScheme` once the design system stabilises.
final ThemeData appTheme = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
);
