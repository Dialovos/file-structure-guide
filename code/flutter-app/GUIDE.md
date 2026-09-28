## TL;DR

The default **Flutter** app layout puts every line of Dart you write in `lib/`, every test in `test/`, every public dependency in `pubspec.yaml`, and the generated platform-specific projects (`android/`, `ios/`, `web/`, `macos/`, `linux/`, `windows/`) at the top level. That's the shape `flutter create` produces and the shape every Flutter article, package, and example assumes. Inside `lib/` is where teams diverge. The recommended convention for non-trivial apps — and the one this guide adopts — is **feature folders**: `lib/main.dart` as the entry point, `lib/app/` for the root `MaterialApp` and theme, `lib/features/<feature>/` for each user-facing feature, `lib/core/` for cross-cutting infrastructure (API client, dependency injection, routing), and `lib/shared/` for widgets/utilities reused across features. `pubspec.yaml` is the load-bearing file: it declares the package name (snake_case, *not* dashes — Dart's one un-negotiable convention), the SDK constraint, dependencies, dev dependencies, and asset bundles. `analysis_options.yaml` configures the linter; the `flutter_lints` package is the Dart team's recommended baseline. Platform directories are auto-generated and committed; you usually edit them only to wire native code or change app icons. The single most common mistake is dumping everything into `lib/screens/` and `lib/widgets/` until those folders sprawl past a hundred files — feature-folder organization scales further with no tooling cost.

## Principles & why

The Flutter / Dart layout is shaped by five principles, each enforced by tooling.

1. **`lib/` is the only Dart code root.** `flutter run`, `flutter test`, and `dart pub publish` all assume `lib/` is the package's source. Anything outside `lib/` (with the exception of `bin/` for executable scripts and `test/`) is invisible to the build. Don't make a sibling `src/` directory — Dart has a built-in `lib/src/` convention for "implementation details not part of the public API," and that's the only `src/` Flutter projects use.
2. **`pubspec.yaml` is the manifest, period.** Package name, SDK constraint, dependencies, assets, fonts — all in one file. There's no `package.json`-style split between dev and runtime configs, no separate manifest for Flutter vs. Dart code. `pub get` reads this file; `flutter run` reads this file; everyone reads this file. Keep it tidy.
3. **Feature folders scale; type folders don't.** A `lib/screens/` folder with 80 screens forces you to remember "what is this screen called?" before you can find it. A `lib/features/checkout/checkout_screen.dart` lets you start with the user-facing concept (checkout) and drill in. The Flutter docs and most production templates (Reso Coder, Very Good Ventures, Bloc library) all converge on this pattern once apps have more than ~5 screens.
4. **`test/` mirrors `lib/`.** A test for `lib/features/home/home_screen.dart` lives at `test/features/home/home_screen_test.dart`. Widget tests, unit tests, and (with the `integration_test/` directory) integration tests all share the structure. The mirror convention keeps "where do I add the test?" trivial.
5. **Platform code is auto-generated, then yours.** `flutter create` regenerates `android/`, `ios/`, etc. from templates. After that they're yours — you can edit `android/app/src/main/AndroidManifest.xml`, add native plugins, change `ios/Runner/Info.plist`. Commit them. Don't re-run `flutter create .` blindly on an existing project; it will overwrite your changes (use `flutter create --platforms=android .` to add a single platform).

A sixth convention worth flagging: Dart enforces `snake_case` for file and package names (`home_screen.dart`, package `my_app`), `lowerCamelCase` for variables/functions, and `UpperCamelCase` for types. The linter will warn on violations. This is one of the only ecosystems where the directory convention (kebab-case for guides) and the package name convention (snake_case for Dart) diverge — that's why this guide's directory is `code/flutter-app/` but the template's `pubspec.yaml` says `name: my_app`.

## When to use

- **Multi-feature Flutter mobile apps** (iOS + Android) where `lib/` would otherwise have 50+ files at the same level.
- **Flutter desktop or web apps** with the same multi-feature problem; the layout is identical regardless of target platform.
- **Apps with state-management beyond `setState`** (Bloc, Riverpod, Provider). Each feature folder owns its `*_controller.dart` / `*_bloc.dart` / `*_notifier.dart` next to the screens that consume it.
- **Teams** where multiple developers ship features in parallel. Feature folders minimize merge conflicts because each developer typically touches one folder.
- **Apps that will eventually need clean architecture.** Feature folders are the gateway: once a feature outgrows a single folder, you sub-divide it into `data/`, `domain/`, `presentation/` *inside* `features/<feature>/` without disturbing the rest of the app.

## When NOT to use

- **Single-screen demos, prototypes, samples.** A flat `lib/` with `main.dart` and a `home_screen.dart` is fine. Adding `features/home/` for one feature is ceremony.
- **Pure Dart packages** (no Flutter dependency). They use a different layout: `lib/<package_name>.dart` as the entry, `lib/src/` for implementation, `example/` for sample usage, no platform directories. See `package:http`, `package:dio`, `package:json_serializable` for examples. Run `dart create -t package <name>` instead of `flutter create`.
- **Plugins / federated plugins.** Flutter plugins have their own structure with `android/`, `ios/`, etc. as *part of the package itself*, plus an `example/` Flutter app. Run `flutter create --template=plugin <name>`.
- **Apps that need monorepo organization** (multiple Flutter apps in one repo). Use Melos or a workspace tool; each Flutter app inside still follows this layout, but the repo root is different.

## Tree diagram

```
my_app/
├── pubspec.yaml
├── README.md
├── LICENSE
├── .gitignore
├── analysis_options.yaml
├── lib/
│   ├── main.dart
│   ├── app/
│   │   ├── app.dart
│   │   └── theme.dart
│   ├── features/
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   └── home_controller.dart
│   │   └── settings/
│   ├── core/
│   │   ├── api/
│   │   └── di/
│   └── shared/
│       └── widgets/
├── test/
│   ├── widget_test.dart
│   └── unit/
├── android/                       ← platform-specific
├── ios/
├── web/
└── assets/
    └── images/
```

## Naming rules

- **Package name** (`pubspec.yaml` `name:`): `snake_case`, lowercase, no dashes, no leading digits. `my_app`, `super_dashboard`, `acme_mobile`. The directory holding the project should match (`my_app/`). This is enforced by `pub` and `flutter`.
- **Dart files**: `snake_case.dart`. `home_screen.dart`, `auth_repository.dart`, `user_model.dart`. The linter (`file_names` rule) enforces this.
- **Class / type names**: `UpperCamelCase`. `HomeScreen`, `AuthRepository`, `UserModel`.
- **Variables, functions, parameters**: `lowerCamelCase`. `currentUser`, `fetchUserProfile()`.
- **Constants**: `lowerCamelCase` (yes, even constants — Effective Dart deliberately broke from the Java convention). `defaultTimeout`, `maxRetries`.
- **Feature folders**: `snake_case`, singular noun for the feature. `lib/features/home/`, `lib/features/checkout/`, `lib/features/user_profile/`. Avoid `lib/features/screens/` (defeats the point) or `lib/features/login_feature/` (redundant `_feature` suffix).
- **Test files**: mirror the source name + `_test.dart`. `lib/features/home/home_screen.dart` → `test/features/home/home_screen_test.dart`.
- **Asset paths in `pubspec.yaml`**: lowercase, hyphens or underscores both work but stay consistent. `assets/images/logo.png`. Reference in code as `'assets/images/logo.png'` (no leading slash).

## Worked example

All screens live in `lib/screens/`, all widgets in `lib/widgets/`, and adding a setting touches both.

1. Create `lib/features/<name>/` for each capability: `home/`, `settings/`.
2. Move each screen with its controller, state, and private widgets: `home_screen.dart`, `home_controller.dart`.
3. Put cross-feature infrastructure in `lib/core/` (API client, dependency injection) and reusable widgets in `lib/shared/widgets/`.
4. Keep `lib/app/` for the root `MaterialApp`, routing, and theme.
5. Mirror the structure in `test/`, and run `flutter analyze && flutter test`.
6. Leave the generated `android/`, `ios/`, and other platform folders in place; edit them only for platform settings.

New work now lands in one feature folder and code review follows feature boundaries.

## Anti-patterns

- **`lib/screens/` and `lib/widgets/` as top-level type folders.** As an app grows, these become unsearchable. A widget for the checkout flow lives next to a widget for the user settings — no relationship between adjacent files. Use `lib/features/<name>/` instead.
- **Putting `main()` in a file named anything other than `main.dart`.** `flutter run` defaults to `lib/main.dart`. You can override with `--target`, but every IDE, every CI, every tutorial assumes `main.dart`. Keep it.
- **Importing across features.** `lib/features/home/` should not `import 'package:my_app/features/checkout/checkout_screen.dart'`. If two features need to share a widget, lift it to `lib/shared/widgets/`. If they need to share business logic, lift it to `lib/core/`. Cross-feature imports are how feature folders silently turn into spaghetti.
- **Hardcoding asset paths as strings in widgets.** Centralize them. Make a `lib/core/assets.dart` with `class AppAssets { static const logo = 'assets/images/logo.png'; }`, or use the `flutter_gen` package to auto-generate typed asset references. String typos in asset paths fail at runtime, not compile time.
- **Editing `android/` or `ios/` files without committing them.** Some teams gitignore these because they "auto-regenerate." They don't — anything you customize (signing config, AndroidManifest changes, Info.plist entries, plugin native code) lives there. Commit the whole platform directory.
- **Skipping `analysis_options.yaml`.** Flutter ships `flutter_lints` as the recommended baseline. Without it, your IDE won't flag missed `await`s, unused imports, or naming-convention violations. One `include: package:flutter_lints/flutter.yaml` line is all it takes.
- **Putting `pubspec.lock` in `.gitignore` for an app.** Apps commit the lockfile (deterministic builds). Libraries / packages don't (they let consumers resolve fresh). Same convention as Cargo / poetry — the difference matters.
- **One giant `lib/utils.dart`.** A 2000-line dumping ground. Split into focused files inside `lib/shared/` or `lib/core/` (`lib/core/extensions/string_extensions.dart`, `lib/shared/format/date_format.dart`).

## Scaling & failure modes

- **State management** choice (Riverpod, Bloc, Provider) matters less than consistency; apply one pattern per feature folder layout.
- **Generated code** (`*.g.dart`, `*.freezed.dart`) should be gitignored or clearly marked; regenerate with `dart run build_runner build`.
- **Platform folders** attract merge conflicts; keep changes to them small and reviewed.
- **Large apps** benefit from a multi-package (melos) layout, splitting `core` and features into packages.

## Variants

- **Feature folders (this guide)** — the most common community convention, taught in the Flutter docs and used in Very Good CLI's generated apps, Reso Coder's templates, and most production codebases.
- **Layered (data / domain / presentation)** — clean architecture at the top level. `lib/data/`, `lib/domain/`, `lib/presentation/` instead of `lib/features/`. Some teams nest *both*: `lib/features/home/data/`, `lib/features/home/domain/`, `lib/features/home/presentation/`. Bigger investment, pays off in large apps.
- **MVC layered** — `lib/models/`, `lib/views/`, `lib/controllers/`. Type folders. Familiar from older mobile frameworks; doesn't scale as well as features.
- **Bloc-pattern flavor** — feature folders, but each feature has a `bloc/` subdirectory (`bloc/home_bloc.dart`, `bloc/home_event.dart`, `bloc/home_state.dart`) following the `flutter_bloc` package's recommended files. Compatible with this guide.
- **Riverpod clean-architecture** — feature folders, with `application/`, `domain/`, `presentation/`, `data/` per feature. Common in apps using Riverpod with code generation (`riverpod_generator`).
- **Modular (`flutter_modular` package)** — each feature is a self-contained "module" with its own router. Stronger isolation; smaller community.
- **Single-package** vs. **multi-package monorepo** (Melos) — large apps split features into their own pub packages and depend on them via path. Out of scope for this guide; see Very Good Ventures' "Very Good Layered Architecture" for an example.

## Adoption checklist

- [ ] `flutter analyze` and `flutter test` pass on a clean clone.
- [ ] `lib/` uses feature folders, with no flat `screens/` or `widgets/` dumping ground.
- [ ] One state-management approach is used across features.
- [ ] Generated files are either ignored or consistently committed.
- [ ] Assets are declared in `pubspec.yaml` and live under `assets/`.

## Real-world projects using this

- **flutter/samples** — the official samples repo. The `experimental/` and `desktop_photo_search/` examples follow feature-folder patterns; `wonderous/` (the Wonderous app source) is a polished feature-folder reference.
- **Very Good CLI generated apps** (`very_good_cli` from Very Good Ventures) — scaffolds a Flutter app with the layered + feature-folder hybrid by default. The "Very Good Layered Architecture" doc is one of the most widely cited references.
- **Reso Coder's clean-architecture template** — the Reso Coder YouTube series popularized clean architecture in Flutter; the public GitHub repo (`ResoCoder/flutter-clean-architecture-course`) is a feature-folder layout with data/domain/presentation per feature.
- **FlutterFire example apps** (`firebase/flutterfire`) — each integration in `examples/` is a feature-folder Flutter app demonstrating one Firebase service.
- **fluttercommunity/plus_plugins** — official plus-plugins; the example apps inside each plugin (`battery_plus/example/`) use the same `lib/main.dart` + feature-folder layout.
- **AppFlowy** (`AppFlowy-IO/AppFlowy`) — production-scale Flutter desktop app; uses feature-folder organization at scale.
- **Wonderous** (`gskinnerTeam/flutter-wonderous-app`) — gskinner's reference design app; widely referenced for animation and structure.

## Migration & references

- **Migrating from flat `lib/` to feature folders**: identify the natural feature boundaries (one per main screen / route). Create `lib/features/<feature>/`. `git mv` the screen files in. Update imports — your IDE's "move file" refactor handles 90 % of this. Run `dart fix --apply` to mop up. Repeat per feature; the migration is incremental.
- **Migrating from MVC (`models/`, `views/`, `controllers/`)** to feature folders: pick a feature, create `lib/features/<feature>/`, move *all* files (model, view, controller) for that feature inside. The MVC folders shrink as you go; eventually you delete them. Easier than the reverse direction.
- **Adding a new feature**: `mkdir lib/features/<name>`. Create `<name>_screen.dart` and `<name>_controller.dart` inside. Add the route in `lib/app/app.dart`. Done. No global registry to update.
- **Adding tests**: mirror the path. `lib/features/home/home_screen.dart` → `test/features/home/home_screen_test.dart`. Run `flutter test`.
- **Adding native code**: edit `android/app/src/main/kotlin/.../MainActivity.kt` for Android, `ios/Runner/AppDelegate.swift` for iOS. Plugins live in their own packages; only platform-customization for *this app* goes in `android/` and `ios/`.
- **References**:
  - Flutter docs — *Code organization* page in the architecture section (docs.flutter.dev/app-architecture).
  - Effective Dart (dart.dev/guides/language/effective-dart) — naming, style, design.
  - `flutter_lints` package — the recommended `analysis_options.yaml` baseline.
  - Very Good Ventures' *Very Good Layered Architecture* blog post — the canonical clean-arch + feature-folder hybrid.
  - Sibling guides: `code/kotlin-android/` (the native-Android equivalent), `code/swift-package/` (iOS-native equivalent for libraries).
