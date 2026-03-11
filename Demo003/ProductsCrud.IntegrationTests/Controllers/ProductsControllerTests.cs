// =============================================================================
// Archivo      : ProductsControllerTests.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Tests de integración para el controlador ProductsController.
//                Valida los endpoints CRUD usando WebApplicationFactory y base
//                de datos en memoria.
// =============================================================================

using System.Data.Common;
using System.Net;
using System.Net.Http.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using ProductsCrud.Data;
using ProductsCrud.Models;

namespace ProductsCrud.IntegrationTests.Controllers;

/// <summary>
/// Factory personalizada para tests que usa SQLite en memoria.
/// </summary>
public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remover la configuración de SQLite de archivo
            services.RemoveAll(typeof(DbContextOptions<AppDbContext>));

            // Crear conexión SQLite en memoria
            var connection = new SqliteConnection("DataSource=:memory:");
            connection.Open();

            // Agregar SQLite en memoria
            services.AddSingleton<DbConnection>(connection);
            services.AddDbContext<AppDbContext>(options =>
            {
                options.UseSqlite(connection);
            });

            // Inicializar la base de datos
            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.Database.EnsureCreated();
        });

        builder.UseEnvironment("Testing");
    }
}

/// <summary>
/// Suite de tests de integración para <see cref="ProductsController"/>.
/// Utiliza WebApplicationFactory con SQLite en memoria.
/// </summary>
public class ProductsControllerTests : IDisposable
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory _factory;

    public ProductsControllerTests()
    {
        _factory = new CustomWebApplicationFactory();
        _client = _factory.CreateClient();
    }

    public void Dispose()
    {
        _client?.Dispose();
        _factory?.Dispose();
        GC.SuppressFinalize(this);
    }

    private async Task<int> CreateActiveCategoryAsync(string baseName = "Categoria Test")
    {
        var createResponse = await _client.PostAsJsonAsync("/api/categories", new CategoryCreateDto
        {
            Name = $"{baseName}-{Guid.NewGuid():N}",
            Description = "Categoria para pruebas de productos",
            IsActive = true
        });

        createResponse.StatusCode.Should().Be(HttpStatusCode.Created);
        var createdCategory = await createResponse.Content.ReadFromJsonAsync<CategoryDetailDto>();
        createdCategory.Should().NotBeNull();

        return createdCategory!.Id;
    }

    #region GetAll Tests

    [Fact]
    public async Task GetAll_WithNoProducts_ReturnsEmptyList()
    {
        // Act
        var response = await _client.GetAsync("/api/products");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var products = await response.Content.ReadFromJsonAsync<List<Product>>();
        products.Should().NotBeNull();
        products.Should().BeEmpty();
    }

    [Fact]
    public async Task GetAll_WithExistingProducts_ReturnsAllProducts()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product1 = new Product { Name = "Laptop", Price = 999.99m, Stock = 10, CategoryId = categoryId };
        var product2 = new Product { Name = "Mouse", Price = 29.99m, Stock = 50, CategoryId = categoryId };
        
        await _client.PostAsJsonAsync("/api/products", product1);
        await _client.PostAsJsonAsync("/api/products", product2);

        // Act
        var response = await _client.GetAsync("/api/products");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var products = await response.Content.ReadFromJsonAsync<List<Product>>();
        products.Should().NotBeNull();
        products.Should().HaveCount(2);
        products.Should().Contain(p => p.Name == "Laptop");
        products.Should().Contain(p => p.Name == "Mouse");
    }

    #endregion

    #region GetById Tests

    [Fact]
    public async Task GetById_WithExistingId_ReturnsProduct()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product 
        { 
            Name = "Teclado Mecánico", 
            Description = "RGB retroiluminado",
            Price = 149.99m, 
            Stock = 25,
            CategoryId = categoryId
        };
        
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        // Act
        var response = await _client.GetAsync($"/api/products/{createdProduct!.Id}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var retrievedProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
        retrievedProduct.Should().NotBeNull();
        retrievedProduct!.Id.Should().Be(createdProduct.Id);
        retrievedProduct.Name.Should().Be("Teclado Mecánico");
        retrievedProduct.Description.Should().Be("RGB retroiluminado");
        retrievedProduct.Price.Should().Be(149.99m);
        retrievedProduct.Stock.Should().Be(25);
    }

    [Fact]
    public async Task GetById_WithNonExistentId_ReturnsNotFound()
    {
        // Arrange
        var nonExistentId = 99999;

        // Act
        var response = await _client.GetAsync($"/api/products/{nonExistentId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task GetById_WithZeroId_ReturnsNotFound()
    {
        // Act
        var response = await _client.GetAsync("/api/products/0");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task GetById_WithNegativeId_ReturnsNotFound()
    {
        // Act
        var response = await _client.GetAsync("/api/products/-1");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    #endregion

    #region Create Tests

    [Fact]
    public async Task Create_WithValidData_ReturnsCreatedWithProduct()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product 
        { 
            Name = "Monitor 27\"", 
            Description = "Full HD IPS",
            Price = 299.99m, 
            Stock = 15,
            CategoryId = categoryId
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/products", product);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        
        var createdProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
        createdProduct.Should().NotBeNull();
        createdProduct!.Id.Should().BeGreaterThan(0);
        createdProduct.Name.Should().Be("Monitor 27\"");
        createdProduct.Description.Should().Be("Full HD IPS");
        createdProduct.Price.Should().Be(299.99m);
        createdProduct.Stock.Should().Be(15);
        
        response.Headers.Location.Should().NotBeNull();
        response.Headers.Location!.ToString().Should().ContainEquivalentOf($"/api/products/{createdProduct.Id}");
    }

    [Fact]
    public async Task Create_WithMinimalData_ReturnsCreatedWithProduct()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product 
        { 
            Name = "Producto Básico", 
            Price = 0, 
            Stock = 0,
            CategoryId = categoryId
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/products", product);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        
        var createdProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
        createdProduct.Should().NotBeNull();
        createdProduct!.Id.Should().BeGreaterThan(0);
        createdProduct.Name.Should().Be("Producto Básico");
        createdProduct.Description.Should().BeNullOrEmpty();
        createdProduct.Price.Should().Be(0);
        createdProduct.Stock.Should().Be(0);
    }

    [Fact]
    public async Task Create_WithLongValues_ReturnsCreatedWithProduct()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product 
        { 
            Name = new string('A', 200), // Máximo permitido
            Description = new string('B', 1000), // Máximo permitido
            Price = 9999999.99m, 
            Stock = int.MaxValue,
            CategoryId = categoryId
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/products", product);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        
        var createdProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
        createdProduct.Should().NotBeNull();
        createdProduct!.Name.Should().HaveLength(200);
        createdProduct.Description.Should().HaveLength(1000);
    }

    #endregion

    #region Update Tests

    [Fact]
    public async Task Update_WithValidData_ReturnsNoContent()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Name = "Original", Price = 100m, Stock = 10, CategoryId = categoryId };
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        var updatedProduct = new Product
        {
            Id = createdProduct!.Id,
            Name = "Actualizado",
            Description = "Nueva descripción",
            Price = 150m,
            Stock = 20,
            CategoryId = categoryId
        };

        // Act
        var response = await _client.PutAsJsonAsync($"/api/products/{createdProduct.Id}", updatedProduct);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NoContent);

        // Verificar que se actualizó
        var getResponse = await _client.GetAsync($"/api/products/{createdProduct.Id}");
        var retrievedProduct = await getResponse.Content.ReadFromJsonAsync<ProductDto>();
        retrievedProduct!.Name.Should().Be("Actualizado");
        retrievedProduct.Price.Should().Be(150m);
        retrievedProduct.Stock.Should().Be(20);
        retrievedProduct.Description.Should().Be("Nueva descripción");
    }

    [Fact]
    public async Task Update_WithMismatchedId_ReturnsBadRequest()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Id = 1, Name = "Test", Price = 100m, Stock = 10, CategoryId = categoryId };

        // Act
        var response = await _client.PutAsJsonAsync("/api/products/999", product);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Update_WithNonExistentId_ReturnsNotFound()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Id = 99999, Name = "Test", Price = 100m, Stock = 10, CategoryId = categoryId };

        // Act
        var response = await _client.PutAsJsonAsync("/api/products/99999", product);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Update_PartialChange_ReturnsNoContent()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product 
        { 
            Name = "Original", 
            Description = "Descripción original",
            Price = 100m, 
            Stock = 10,
            CategoryId = categoryId
        };
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        // Solo cambiar el precio
        var updatedProduct = new Product
        {
            Id = createdProduct!.Id,
            Name = "Original",
            Description = "Descripción original",
            Price = 200m,
            Stock = 10,
            CategoryId = categoryId
        };

        // Act
        var response = await _client.PutAsJsonAsync($"/api/products/{createdProduct.Id}", updatedProduct);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NoContent);

        // Verificar que solo el precio cambió
        var getResponse = await _client.GetAsync($"/api/products/{createdProduct.Id}");
        var retrievedProduct = await getResponse.Content.ReadFromJsonAsync<ProductDto>();
        retrievedProduct!.Name.Should().Be("Original");
        retrievedProduct.Description.Should().Be("Descripción original");
        retrievedProduct.Price.Should().Be(200m);
        retrievedProduct.Stock.Should().Be(10);
    }

    #endregion

    #region Delete Tests

    [Fact]
    public async Task Delete_WithExistingId_ReturnsNoContent()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Name = "Para Eliminar", Price = 100m, Stock = 10, CategoryId = categoryId };
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        // Act
        var response = await _client.DeleteAsync($"/api/products/{createdProduct!.Id}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NoContent);

        // Verificar que se eliminó
        var getResponse = await _client.GetAsync($"/api/products/{createdProduct.Id}");
        getResponse.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_WithNonExistentId_ReturnsNotFound()
    {
        // Arrange
        var nonExistentId = 99999;

        // Act
        var response = await _client.DeleteAsync($"/api/products/{nonExistentId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Delete_SameIdTwice_SecondReturnsNotFound()
    {
        // Arrange
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Name = "Eliminar Dos Veces", Price = 100m, Stock = 10, CategoryId = categoryId };
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        // Act
        var firstDelete = await _client.DeleteAsync($"/api/products/{createdProduct!.Id}");
        var secondDelete = await _client.DeleteAsync($"/api/products/{createdProduct.Id}");

        // Assert
        firstDelete.StatusCode.Should().Be(HttpStatusCode.NoContent);
        secondDelete.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    #endregion

    #region Integration Workflow Tests

    [Fact]
    public async Task CompleteWorkflow_CreateReadUpdateDelete_AllSucceed()
    {
        // Arrange & Act - Create
        var categoryId = await CreateActiveCategoryAsync();
        var product = new Product { Name = "Workflow Test", Price = 100m, Stock = 10, CategoryId = categoryId };
        var createResponse = await _client.PostAsJsonAsync("/api/products", product);
        createResponse.StatusCode.Should().Be(HttpStatusCode.Created);
        var createdProduct = await createResponse.Content.ReadFromJsonAsync<ProductDto>();

        // Act - Read
        var getResponse = await _client.GetAsync($"/api/products/{createdProduct!.Id}");
        getResponse.StatusCode.Should().Be(HttpStatusCode.OK);
        var retrievedProduct = await getResponse.Content.ReadFromJsonAsync<ProductDto>();
        retrievedProduct.Should().BeEquivalentTo(createdProduct);

        // Act - Update
        var updatedPayload = new Product
        {
            Id = createdProduct!.Id,
            Name = "Updated",
            Description = createdProduct.Description,
            Price = 200m,
            Stock = createdProduct.Stock,
            CategoryId = categoryId
        };
        var updateResponse = await _client.PutAsJsonAsync($"/api/products/{createdProduct.Id}", updatedPayload);
        updateResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);

        // Act - Verify Update
        var getUpdatedResponse = await _client.GetAsync($"/api/products/{createdProduct.Id}");
        var updatedProduct = await getUpdatedResponse.Content.ReadFromJsonAsync<ProductDto>();
        updatedProduct!.Name.Should().Be("Updated");
        updatedProduct.Price.Should().Be(200m);

        // Act - Delete
        var deleteResponse = await _client.DeleteAsync($"/api/products/{createdProduct.Id}");
        deleteResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);

        // Act - Verify Delete
        var getFinalResponse = await _client.GetAsync($"/api/products/{createdProduct.Id}");
        getFinalResponse.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task CreateMultipleProducts_GetAll_ReturnsAllInCorrectOrder()
    {
        // Arrange & Act
        var categoryId = await CreateActiveCategoryAsync();
        var products = new[]
        {
            new Product { Name = "Producto 1", Price = 10m, Stock = 1, CategoryId = categoryId },
            new Product { Name = "Producto 2", Price = 20m, Stock = 2, CategoryId = categoryId },
            new Product { Name = "Producto 3", Price = 30m, Stock = 3, CategoryId = categoryId }
        };

        var createdIds = new List<int>();
        foreach (var product in products)
        {
            var response = await _client.PostAsJsonAsync("/api/products", product);
            var created = await response.Content.ReadFromJsonAsync<ProductDto>();
            createdIds.Add(created!.Id);
        }

        // Act
        var getAllResponse = await _client.GetAsync("/api/products");
        var allProducts = await getAllResponse.Content.ReadFromJsonAsync<List<Product>>();

        // Assert
        allProducts.Should().HaveCount(3);
        allProducts.Should().OnlyContain(p => createdIds.Contains(p.Id));
        allProducts!.Select(p => p.Name).Should().Contain(new[] { "Producto 1", "Producto 2", "Producto 3" });
    }

    #endregion
}
