plugins {
    `java-library`
}

dependencies {
    api(project(":core"))
    testImplementation(libs.junit.jupiter)
}
