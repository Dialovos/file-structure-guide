// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift
// required to build this package. SwiftPM uses it to select which
// PackageDescription API to expose.

import PackageDescription

let package = Package(
    name: "MyPackage",
    platforms: [
        .macOS(.v13),
        .iOS(.v16),
        .tvOS(.v16),
        .watchOS(.v9),
    ],
    products: [
        // The library product: external consumers add this package
        // and write `import MyPackage`.
        .library(
            name: "MyPackage",
            targets: ["MyPackage"]
        ),
        // The CLI executable that demonstrates calling MyPackage.
        .executable(
            name: "mypackage-cli",
            targets: ["MyPackageCLI"]
        ),
    ],
    dependencies: [
        // No external dependencies in the template. Add them like:
        // .package(url: "https://github.com/apple/swift-argument-parser", from: "1.3.0"),
    ],
    targets: [
        .target(
            name: "MyPackage",
            dependencies: []
        ),
        .executableTarget(
            name: "MyPackageCLI",
            dependencies: ["MyPackage"]
        ),
        .testTarget(
            name: "MyPackageTests",
            dependencies: ["MyPackage"]
        ),
    ]
)
