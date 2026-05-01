using MySolution.Core;

// Minimal API stub. Replace with your real WebApplication.CreateBuilder
// pipeline (controllers, MapGet, middleware) as the project grows.
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<Greeter>();

var app = builder.Build();

app.MapGet("/", (Greeter greeter, string? name) => greeter.Greet(name));

app.Run();
