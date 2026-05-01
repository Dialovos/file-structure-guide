plugins {
    alias(libs.plugins.myapp.android.feature)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.example.myapp.feature.home"
}

dependencies {
    implementation(project(":core:domain"))
    implementation(project(":core:designsystem"))

    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
}
