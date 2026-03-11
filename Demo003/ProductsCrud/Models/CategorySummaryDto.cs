// =============================================================================
// Archivo      : CategorySummaryDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO resumido para representar una categoría en listados.
//                Incluye el conteo de productos asociados.
// =============================================================================

namespace ProductsCrud.Models;

/// <summary>
/// DTO resumido utilizado para mostrar categorías en listados.
/// Incluye información básica y el número de productos asociados.
/// </summary>
public class CategorySummaryDto
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
    /// Indica si la categoría está activa.
    /// </summary>
    public bool IsActive { get; set; }

    /// <summary>
    /// Número de productos asociados a esta categoría.
    /// </summary>
    public int ProductsCount { get; set; }
}