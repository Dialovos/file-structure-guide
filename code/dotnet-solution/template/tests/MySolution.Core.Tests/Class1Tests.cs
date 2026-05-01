using Xunit;

namespace MySolution.Core.Tests;

public class GreeterTests
{
    [Fact]
    public void Greet_ReturnsHelloWithName()
    {
        var sut = new Greeter();
        Assert.Equal("hello, alice", sut.Greet("alice"));
    }

    [Fact]
    public void Greet_FallsBackToWorldOnEmptyInput()
    {
        var sut = new Greeter();
        Assert.Equal("hello, world", sut.Greet(""));
        Assert.Equal("hello, world", sut.Greet(null));
    }
}
