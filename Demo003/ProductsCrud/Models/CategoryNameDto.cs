// =============================================================================
// Archivo      : CategoryNameDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO mínimo para listar categorías devolviendo solo el nombre.
// =============================================================================

namespace ProductsCrud.Models;

/// <summary>
/// DTO mínimo de categoría para respuestas que solo requieren el nombre.
/// </summary>
public class CategoryNameDto
{
    /// <summary>
    /// Nombre de la categoría.
    /// </summary>
    public string Name { get; set; } = string.Empty;
}
