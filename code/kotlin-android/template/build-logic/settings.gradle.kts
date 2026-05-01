// build-logic is a sub-build that hosts the convention plugins. It
// has its own settings.gradle.kts so it can be developed independently
// of the main build's plugin classpath.
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
    versionCatalogs {
        create("libs") {
            from(files("../gradle/libs.versions.toml"))
        }
    }
}

rootProject.name = "build-logic"

include(":convention")
