plugins {
    application
}

application {
    mainClass.set("com.example.app.App")
}

dependencies {
    implementation(project(":api"))
    implementation(project(":core"))
    testImplementation(libs.junit.jupiter)
}
