plugins {
    alias(libs.plugins.myapp.android.feature)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.example.myapp.feature.settings"
}

dependencies {
    implementation(project(":core:domain"))
    implementation(project(":core:designsystem"))
}
