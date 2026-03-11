using Microsoft.EntityFrameworkCore;
using ProductsCrud.Data;
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers(options =>
{
    options.ReturnHttpNotAcceptable = true; // Negociación de contenido estricta
})
.AddXmlDataContractSerializerFormatters(); // Soporte para XML

builder.Services.AddProblemDetails(); // Respuesta de error estandarizada (RFC 7807)
builder.Services.AddOpenApi();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

// Aplicar migraciones automáticamente en desarrollo
if (app.Environment.IsDevelopment())
{
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();

    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.UseExceptionHandler(); // Middleware de Problem Details
app.UseStatusCodePages(); // Páginas de código de estado con Problem Details

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();

// Hacer la clase Program visible para los tests de integración
public partial class Program { }
