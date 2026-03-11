// =============================================================================
// Archivo      : CategoriesController.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Controlador REST que expone los endpoints CRUD para la entidad
//                Category. Utiliza Entity Framework Core para el acceso a datos.
// =============================================================================

using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProductsCrud.Data;
using ProductsCrud.Models;

namespace ProductsCrud.Controllers;

/// <summary>
/// Controlador de la API para la gestión de categorías.
/// Expone operaciones CRUD sobre el recurso <see cref="Category"/>.
/// Ruta base: <c>api/categories</c>.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class CategoriesController(AppDbContext db) : ControllerBase
{
    /// <summary>
    /// Obtiene la lista de categorías, opcionalmente filtradas por estado activo.
    /// </summary>
    /// <param name="isActive">Si se especifica, filtra las categorías por estado activo.</param>
    /// <returns>Lista de categorías en formato resumido.</returns>
    /// <response code="200">Retorna la lista de categorías.</response>
    [HttpGet]
    [ProducesResponseType(typeof(List<CategoryNameDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(bool? isActive = null)
    {
        var query = db.Categories.AsQueryable();

        if (isActive.HasValue)
        {
            query = query.Where(c => c.IsActive == isActive.Value);
        }

        var categories = await query
            .Select(c => new CategoryNameDto
            {
                Name = c.Name
            })
            .ToListAsync();

        return Ok(categories);
    }

    /// <summary>
    /// Obtiene una categoría por su identificador único con detalles completos.
    /// </summary>
    /// <param name="id">Identificador de la categoría.</param>
    /// <returns>La categoría con sus productos asociados.</returns>
    /// <response code="200">Retorna la categoría encontrada.</response>
    /// <response code="404">No existe una categoría con el id indicado.</response>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(CategoryDetailDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(int id)
    {
        var category = await db.Categories
            .Include(c => c.Products)
            .FirstOrDefaultAsync(c => c.Id == id);

        if (category is null)
        {
            return NotFound();
        }

        var dto = new CategoryDetailDto
        {
            Id = category.Id,
            Name = category.Name,
            Description = category.Description,
            IsActive = category.IsActive,
            Products = category.Products.Select(p => new ProductSummaryDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            }).ToList()
        };

        return Ok(dto);
    }

    /// <summary>
    /// Crea una nueva categoría.
    /// </summary>
    /// <param name="dto">Datos de la categoría a crear.</param>
    /// <returns>La categoría creada con su identificador asignado.</returns>
    /// <response code="201">Categoría creada exitosamente.</response>
    /// <response code="400">Datos no válidos.</response>
    [HttpPost]
    [ProducesResponseType(typeof(CategoryDetailDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(CategoryCreateDto dto)
    {
        var category = new Category
        {
            Name = dto.Name,
            Description = dto.Description,
            IsActive = dto.IsActive
        };

        db.Categories.Add(category);
        await db.SaveChangesAsync();

        var resultDto = new CategoryDetailDto
        {
            Id = category.Id,
            Name = category.Name,
            Description = category.Description,
            IsActive = category.IsActive,
            Products = new List<ProductSummaryDto>()
        };

        return CreatedAtAction(nameof(GetById), new { id = category.Id }, resultDto);
    }

    /// <summary>
    /// Actualiza una categoría existente.
    /// </summary>
    /// <param name="id">Identificador de la categoría a actualizar.</param>
    /// <param name="dto">Datos actualizados de la categoría.</param>
    /// <returns>Sin contenido si la operación fue exitosa.</returns>
    /// <response code="204">Categoría actualizada correctamente.</response>
    /// <response code="404">No existe una categoría con el id indicado.</response>
    /// <response code="400">Datos no válidos.</response>
    [HttpPut("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Update(int id, CategoryUpdateDto dto)
    {
        var category = await db.Categories.FindAsync(id);
        if (category is null)
        {
            return NotFound();
        }

        if (dto.Name is not null)
        {
            category.Name = dto.Name;
        }

        if (dto.Description is not null)
        {
            category.Description = dto.Description;
        }

        if (dto.IsActive.HasValue)
        {
            category.IsActive = dto.IsActive.Value;
        }

        await db.SaveChangesAsync();

        return NoContent();
    }

    /// <summary>
    /// Elimina una categoría (soft delete si no tiene productos, conflicto si tiene).
    /// </summary>
    /// <param name="id">Identificador de la categoría a eliminar.</param>
    /// <returns>Sin contenido si se eliminó correctamente.</returns>
    /// <response code="204">Categoría eliminada correctamente.</response>
    /// <response code="404">No existe una categoría con el id indicado.</response>
    /// <response code="409">No se puede eliminar porque tiene productos asociados.</response>
    [HttpDelete("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> Delete(int id)
    {
        var category = await db.Categories
            .Include(c => c.Products)
            .FirstOrDefaultAsync(c => c.Id == id);

        if (category is null)
        {
            return NotFound();
        }

        if (category.Products.Any())
        {
            return Conflict(new ProblemDetails
            {
                Status = 409,
                Title = "No se puede eliminar la categoría",
                Detail = "La categoría tiene productos asociados y no puede ser eliminada."
            });
        }

        // Soft delete: marcar como inactiva en lugar de eliminar físicamente
        category.IsActive = false;
        await db.SaveChangesAsync();

        return NoContent();
    }
}