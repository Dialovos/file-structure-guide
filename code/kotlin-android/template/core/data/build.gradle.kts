plugins {
    alias(libs.plugins.myapp.android.library)
}

android {
    namespace = "com.example.myapp.core.data"
}

dependencies {
    implementation(project(":core:domain"))
    implementation(project(":core:network"))

    implementation(libs.androidx.core.ktx)
    implementation(libs.kotlinx.coroutines.android)
}
