namespace MySolution.Core;

/// <summary>
/// A trivial example type illustrating the canonical
/// <c>src/&lt;Project&gt;/</c> layout. Replace with your real domain
/// types as you grow the project.
/// </summary>
public class Greeter
{
    /// <summary>
    /// Returns a friendly greeting. Falls back to "world" if
    /// <paramref name="name"/> is null or whitespace.
    /// </summary>
    public string Greet(string? name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            name = "world";
        }
        return $"hello, {name}";
    }
}
