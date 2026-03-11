using DemoProductosApi.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Configurar EF Core con LocalDB
builder.Services.AddDbContext<ProductosDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("ProductosDb")));

builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalar();
}

app.UseHttpsRedirection();

// CRUD Productos
app.MapGet("/api/productos", async (ProductosDbContext db) => await db.Productos.ToListAsync());
app.MapGet("/api/productos/{id}", async (int id, ProductosDbContext db) => await db.Productos.FindAsync(id) is Producto p ? Results.Ok(p) : Results.NotFound());
app.MapPost("/api/productos", async (Producto producto, ProductosDbContext db) => {
    db.Productos.Add(producto);
    await db.SaveChangesAsync();
    return Results.Created($"/api/productos/{producto.Id}", producto);
});
app.MapPut("/api/productos/{id}", async (int id, Producto input, ProductosDbContext db) => {
    var producto = await db.Productos.FindAsync(id);
    if (producto is null) return Results.NotFound();
    producto.Nombre = input.Nombre;
    producto.Precio = input.Precio;
    producto.Stock = input.Stock;
    await db.SaveChangesAsync();
    return Results.NoContent();
});
app.MapDelete("/api/productos/{id}", async (int id, ProductosDbContext db) => {
    var producto = await db.Productos.FindAsync(id);
    if (producto is null) return Results.NotFound();
    db.Productos.Remove(producto);
    await db.SaveChangesAsync();
    return Results.NoContent();
});

app.Run();
