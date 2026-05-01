import com.android.build.gradle.LibraryExtension
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.kotlin.dsl.configure

/**
 * Convention plugin shared by every Android *library* module
 * (`core:*`, `feature:*`). Apply via:
 *
 *     plugins { alias(libs.plugins.myapp.android.library) }
 *
 * Configures compileSdk, minSdk, the Kotlin JVM toolchain, and
 * common AndroidX dependencies once per repo.
 */
class AndroidLibraryConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        with(pluginManager) {
            apply("com.android.library")
            apply("org.jetbrains.kotlin.android")
        }

        extensions.configure<LibraryExtension> {
            compileSdk = 34
            defaultConfig {
                minSdk = 24
            }
            compileOptions {
                sourceCompatibility = org.gradle.api.JavaVersion.VERSION_17
                targetCompatibility = org.gradle.api.JavaVersion.VERSION_17
            }
        }
    }
}
