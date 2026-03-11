// =============================================================================
// Archivo      : ProductsController.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Controlador REST que expone los endpoints CRUD para la entidad
//                Product. Utiliza Entity Framework Core para el acceso a datos.
// =============================================================================

using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProductsCrud.Data;
using ProductsCrud.Models;

namespace ProductsCrud.Controllers;

/// <summary>
/// Controlador de la API para la gestión de productos.
/// Expone operaciones CRUD sobre el recurso <see cref="Product"/>.
/// Ruta base: <c>api/products</c>.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ProductsController(AppDbContext db) : ControllerBase
{
    /// <summary>
    /// Obtiene la lista completa de productos.
    /// </summary>
    /// <returns>Colección con todos los productos registrados y enlaces HATEOAS.</returns>
    /// <response code="200">Retorna la lista de productos.</response>
    [HttpGet(Name = nameof(GetAll))]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll()
    {
        // Incluir el cliente para mostrar su nombre en la respuesta
        var products = await db.Products
            .Include(p => p.Cliente)
            .ToListAsync();
        var dtos = products.Select(p => CreateLinksForProduct(ProductDto.FromProduct(p))).ToList();
        return Ok(dtos);
    }

    /// <summary>
    /// Obtiene un producto por su identificador único.
    /// </summary>
    /// <param name="id">Identificador del producto.</param>
    /// <returns>El producto correspondiente al <paramref name="id"/> indicado con enlaces HATEOAS.</returns>
    /// <response code="200">Retorna el producto encontrado.</response>
    /// <response code="404">No existe un producto con el <paramref name="id"/> indicado.</response>
    [HttpGet("{id}", Name = nameof(GetById))]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        // Incluir el cliente para mostrar su nombre en la respuesta
        var product = await db.Products
            .Include(p => p.Cliente)
            .FirstOrDefaultAsync(p => p.Id == id);
        if (product is null)
            return NotFound(new ProblemDetails { Status = 404, Title = "Producto no encontrado.", Detail = $"El producto con Id {id} no existe." });

        return Ok(CreateLinksForProduct(ProductDto.FromProduct(product)));
    }

    /// <summary>
    /// Crea un nuevo producto.
    /// </summary>
    /// <param name="product">Datos del producto a registrar.</param>
    /// <returns>El producto recién creado con su identificador asignado y enlaces HATEOAS.</returns>
    /// <response code="201">Producto creado exitosamente.</response>
    /// <response code="400">Modelo no válido o categoría inválida.</response>
    [HttpPost(Name = nameof(Create))]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductDto>> Create(Product product)
    {
        // Validar que la categoría existe y está activa
        var category = await db.Categories.FindAsync(product.CategoryId);
        if (category is null || !category.IsActive)
        {
            return BadRequest(new ProblemDetails { Status = 400, Title = "Categoría inválida", Detail = "La categoría especificada no existe o no está activa." });
        }

        // Validar que el cliente existe y está activo
        var cliente = await db.Clientes.FindAsync(product.ClienteId);
        if (cliente is null || !cliente.Activo)
        {
            return BadRequest(new ProblemDetails { Status = 400, Title = "Cliente inválido", Detail = "El cliente especificado no existe o no está activo." });
        }

        db.Products.Add(product);
        await db.SaveChangesAsync();

        // Cargar la navegación del cliente para incluir su nombre en la respuesta
        product.Cliente = cliente;
        var dto = CreateLinksForProduct(ProductDto.FromProduct(product));

        return CreatedAtAction(nameof(GetById), new { id = product.Id }, dto);
    }

    /// <summary>
    /// Actualiza completamente un producto existente.
    /// </summary>
    /// <param name="id">Identificador del producto a actualizar.</param>
    /// <param name="product">Datos actualizados del producto. El campo <c>Id</c> debe coincidir con <paramref name="id"/>.</param>
    /// <returns>Sin contenido si la operación fue exitosa.</returns>
    /// <response code="204">Producto actualizado correctamente.</response>
    /// <response code="400">El <paramref name="id"/> no coincide con el <c>Id</c> del producto o categoría inválida.</response>
    /// <response code="404">No existe un producto con el <paramref name="id"/> indicado.</response>
    [HttpPut("{id}", Name = nameof(Update))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(int id, Product product)
    {
        if (id != product.Id)
            return BadRequest(new ProblemDetails { Status = 400, Title = "Id no coincide", Detail = $"El Id de la URL ({id}) no coincide con el Id del cuerpo ({product.Id})." });

        // Validar que la categoría existe y está activa
        var category = await db.Categories.FindAsync(product.CategoryId);
        if (category is null || !category.IsActive)
        {
            return BadRequest(new ProblemDetails { Status = 400, Title = "Categoría inválida", Detail = "La categoría especificada no existe o no está activa." });
        }

        // Validar que el cliente existe y está activo
        var cliente = await db.Clientes.FindAsync(product.ClienteId);
        if (cliente is null || !cliente.Activo)
        {
            return BadRequest(new ProblemDetails { Status = 400, Title = "Cliente inválido", Detail = "El cliente especificado no existe o no está activo." });
        }

        db.Entry(product).State = EntityState.Modified;

        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!await db.Products.AnyAsync(p => p.Id == id))
                return NotFound(new ProblemDetails { Status = 404, Title = "No encontrado", Detail = $"No se encontró un producto con Id {id}." });
            throw;
        }

        return NoContent();
    }

    /// <summary>
    /// Elimina un producto.
    /// </summary>
    /// <param name="id">El ID del producto a eliminar.</param>
    /// <response code="204">Producto eliminado exitosamente.</response>
    /// <response code="404">Producto no encontrado.</response>
    [HttpDelete("{id}", Name = nameof(Delete))]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id)
    {
        var product = await db.Products.FindAsync(id);
        if (product == null)
            return NotFound(new ProblemDetails { Status = 404, Title = "No encontrado.", Detail = $"Producto con id {id} no encontrado para eliminar." });

        db.Products.Remove(product);
        await db.SaveChangesAsync();

        return NoContent();
    }

    private ProductDto CreateLinksForProduct(ProductDto dto)
    {
        dto.Links.Add(new LinkDto(Url.Link(nameof(GetById), new { id = dto.Id })!, "self", "GET"));
        dto.Links.Add(new LinkDto(Url.Link(nameof(Update), new { id = dto.Id })!, "update_product", "PUT"));
        dto.Links.Add(new LinkDto(Url.Link(nameof(Delete), new { id = dto.Id })!, "delete_product", "DELETE"));
        return dto;
    }
}
