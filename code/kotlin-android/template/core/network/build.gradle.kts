plugins {
    alias(libs.plugins.myapp.android.library)
}

android {
    namespace = "com.example.myapp.core.network"
}

dependencies {
    api(libs.retrofit.core)
    api(libs.okhttp.core)
}
