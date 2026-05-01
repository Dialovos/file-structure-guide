# Flutter app — template

A `cp -r`-able starter for a Flutter app using the feature-folder
layout. Entry point in `lib/main.dart`, root widget and theme in
`lib/app/`, one feature per directory in `lib/features/`,
cross-cutting infrastructure in `lib/core/`, reusable widgets in
`lib/shared/`.

## What lives where

- **`lib/main.dart`** — entry point. Tiny: `runApp(const MyApp())`.
- **`lib/app/`** — `MyApp` (`MaterialApp` + theme + routing). The
  closest thing to "global app state."
- **`lib/features/<feature>/`** — one folder per user-facing feature.
  `home/`, `settings/`. Add `<feature>_screen.dart` and
  `<feature>_controller.dart` (or `_bloc.dart` / `_notifier.dart`).
- **`lib/core/`** — infrastructure. `api/` for the HTTP client and
  models, `di/` for dependency injection, add `routing/`, `storage/`,
  etc. as needed.
- **`lib/shared/widgets/`** — widgets used by 2+ features.
- **`test/`** — mirrors `lib/`. `widget_test.dart` is the smoke test;
  add `test/features/<feature>/<file>_test.dart` next to each feature.
- **`assets/images/`** — declared in `pubspec.yaml` under `flutter:
  assets:`. Reference as `'assets/images/<file>.png'`.

## Platform directories

`android/`, `ios/`, `web/` are placeholders here (`.gitkeep`). Run

```bash
flutter create --org com.example --project-name my_app .
```

at the repo root to generate the real platform projects. After that
they're yours — commit them, edit native config (signing,
manifests, plist) inside, don't blindly re-run `flutter create`.

To add a single platform later:

```bash
flutter create --platforms=linux .
```

## What to rename

- `pubspec.yaml` `name:` — `my_app` → your snake_case package name.
- `pubspec.yaml` `description:`, `version:`.
- `lib/app/app.dart` — `MyApp` class name and the title in
  `MaterialApp(title: ...)`.
- `test/widget_test.dart` — the `import 'package:my_app/...'` line
  needs to match your new package name.
- `LICENSE` — `{{YEAR}}` and `{{NAME}}`.
- The directory holding the project should match `name:` in
  `pubspec.yaml` (`my_app/`). Dart enforces snake_case here.

## First run

```bash
flutter pub get          # install dependencies
flutter run              # run on the connected device / emulator
flutter test             # run unit + widget tests
flutter analyze          # run the linter (uses analysis_options.yaml)
```

## Adding a feature

```bash
mkdir lib/features/<name>
# Create:
#   lib/features/<name>/<name>_screen.dart
#   lib/features/<name>/<name>_controller.dart
# Wire the route in lib/app/app.dart.
# Add tests in test/features/<name>/.
```

No global registry to update. The new feature is just a directory.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout, including
  variants (Bloc, Riverpod, clean architecture).
- `../kotlin-android/` — the native-Android equivalent if you're
  comparing.
- The Flutter docs at docs.flutter.dev — *App architecture* page is
  the canonical reference.
- Effective Dart at dart.dev/guides/language/effective-dart for
  Dart-specific naming and style rules.
