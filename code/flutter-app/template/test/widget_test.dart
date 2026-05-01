import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:my_app/app/app.dart';

void main() {
  testWidgets('Home screen renders the greeting', (tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('Home'), findsOneWidget);
    expect(find.textContaining('world'), findsOneWidget);
  });
}
