```
my-project/
├── settings.gradle.kts
├── build.gradle.kts                ← root (plugins, repositories, shared deps)
├── gradle.properties
├── gradle/
│   ├── wrapper/
│   │   ├── gradle-wrapper.jar
│   │   └── gradle-wrapper.properties
│   └── libs.versions.toml          ← version catalog
├── gradlew
├── gradlew.bat
├── README.md
├── core/
│   ├── build.gradle.kts
│   └── src/main/java/...
├── api/
│   ├── build.gradle.kts
│   └── src/main/java/...
└── app/
    ├── build.gradle.kts
    └── src/main/java/...
```
