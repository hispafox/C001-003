// =============================================================================
// Archivo      : CategoryDetailDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO detallado para representar una categoría con sus productos.
//                Incluye toda la información de la categoría y lista de productos.
// =============================================================================

namespace ProductsCrud.Models;

/// <summary>
/// DTO detallado utilizado para mostrar una categoría con toda su información
/// y la lista completa de productos asociados.
/// </summary>
public class CategoryDetailDto
{
    /// <summary>
    /// Identificador único de la categoría.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre de la categoría.
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Descripción de la categoría.
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Indica si la categoría está activa.
    /// </summary>
    public bool IsActive { get; set; }

    /// <summary>
    /// Lista de productos asociados a esta categoría.
    /// Cada producto se representa con información resumida.
    /// </summary>
    public List<ProductSummaryDto> Products { get; set; } = new List<ProductSummaryDto>();
}

/// <summary>
/// DTO resumido para representar un producto en el contexto de una categoría.
/// Incluye información básica del producto.
/// </summary>
public class ProductSummaryDto
{
    /// <summary>
    /// Identificador único del producto.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre del producto.
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Precio del producto.
    /// </summary>
    public decimal Price { get; set; }
}