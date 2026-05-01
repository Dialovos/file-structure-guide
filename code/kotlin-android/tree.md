```
MyApp/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle/
│   ├── libs.versions.toml
│   └── wrapper/...
├── build-logic/                    ← convention plugins for build logic
│   └── convention/
│       └── src/main/kotlin/
├── app/
│   ├── build.gradle.kts
│   └── src/main/...
├── feature/
│   ├── home/
│   │   ├── build.gradle.kts
│   │   └── src/main/...
│   └── settings/
└── core/
    ├── data/
    ├── domain/
    ├── designsystem/
    └── network/
```
