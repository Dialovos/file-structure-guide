plugins {
    alias(libs.plugins.myapp.android.library)
}

android {
    namespace = "com.example.myapp.core.domain"
}

dependencies {
    implementation(libs.kotlinx.coroutines.android)
}
