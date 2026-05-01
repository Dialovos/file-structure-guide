import XCTest
@testable import MyPackage

final class MyPackageTests: XCTestCase {
    func testGreetWithName() {
        let sut = MyPackage()
        XCTAssertEqual(sut.greet("alice"), "hello, alice")
    }

    func testGreetFallsBackToWorld() {
        let sut = MyPackage()
        XCTAssertEqual(sut.greet(""), "hello, world")
        XCTAssertEqual(sut.greet("   "), "hello, world")
    }
}
