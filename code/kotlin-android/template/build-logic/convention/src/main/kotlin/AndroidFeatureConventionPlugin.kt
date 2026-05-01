import org.gradle.api.Plugin
import org.gradle.api.Project

/**
 * Convention plugin for `feature:*` modules. Layers Compose +
 * navigation + DI defaults on top of `myapp.android.library`.
 *
 * Real implementations would also wire ViewModel / Hilt deps; this
 * template stays minimal so the structure stays readable.
 */
class AndroidFeatureConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        pluginManager.apply("myapp.android.library")
        // Add feature-specific defaults here, e.g. Compose enablement,
        // Hilt, kotlinx-coroutines.
    }
}
