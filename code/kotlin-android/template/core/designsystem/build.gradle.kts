plugins {
    alias(libs.plugins.myapp.android.library)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.example.myapp.core.designsystem"
}

dependencies {
    api(platform(libs.androidx.compose.bom))
    api(libs.androidx.compose.ui)
    api(libs.androidx.compose.material3)
    api(libs.androidx.compose.ui.tooling.preview)
}
