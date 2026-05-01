using MySolution.Core;

namespace MySolution.Cli;

/// <summary>
/// CLI entry point. The example takes one optional --name argument
/// and prints a greeting via <see cref="Greeter"/>.
/// </summary>
internal static class Program
{
    public static int Main(string[] args)
    {
        var name = args.Length > 0 ? args[0] : null;
        var greeter = new Greeter();
        Console.WriteLine(greeter.Greet(name));
        return 0;
    }
}
