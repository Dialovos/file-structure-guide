import com.android.build.gradle.internal.dsl.BaseAppModuleExtension
import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.kotlin.dsl.configure

/**
 * Convention plugin for the single `:app` Android *application*
 * module. Wraps `com.android.application` + Kotlin together so the
 * app's build script stays small.
 */
class AndroidApplicationConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        with(pluginManager) {
            apply("com.android.application")
            apply("org.jetbrains.kotlin.android")
        }

        extensions.configure<BaseAppModuleExtension> {
            compileSdk = 34
            defaultConfig {
                minSdk = 24
                targetSdk = 34
                versionCode = 1
                versionName = "0.1.0"
            }
            compileOptions {
                sourceCompatibility = org.gradle.api.JavaVersion.VERSION_17
                targetCompatibility = org.gradle.api.JavaVersion.VERSION_17
            }
        }
    }
}
