import Foundation
import MyPackage

// Minimal CLI entry point. Replace the manual arg parsing with
// swift-argument-parser when you add real flags:
//
//   .package(url: "https://github.com/apple/swift-argument-parser", from: "1.3.0")
//   .executableTarget(name: "MyPackageCLI", dependencies: ["MyPackage", .product(name: "ArgumentParser", package: "swift-argument-parser")])
let name = CommandLine.arguments.dropFirst().first ?? "world"
let pkg = MyPackage()
print(pkg.greet(name))
