import 'package:flutter/material.dart';

import '../features/home/home_screen.dart';
import 'theme.dart';

/// Root [MaterialApp]. Owns the theme, routing, and any app-wide
/// providers. Keep this file small — push real logic into features.
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: appTheme,
      home: const HomeScreen(),
    );
  }
}
