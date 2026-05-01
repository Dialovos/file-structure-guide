import 'package:flutter/material.dart';

import 'home_controller.dart';

/// Home screen — first thing the user sees. Replace the body with
/// the real UI. Keep widget code here; push state to
/// [HomeController].
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final controller = HomeController();
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: Text('Hello, ${controller.greetingTarget}!'),
      ),
    );
  }
}
