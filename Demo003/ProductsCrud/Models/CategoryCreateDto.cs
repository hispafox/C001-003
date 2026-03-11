// =============================================================================
// Archivo      : CategoryCreateDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO para la creación de una nueva categoría.
//                Contiene solo los campos necesarios para crear una categoría.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// DTO utilizado para crear una nueva categoría.
/// Incluye validaciones para asegurar la integridad de los datos.
/// </summary>
public class CategoryCreateDto
{
    /// <summary>
    /// Nombre de la categoría. Campo obligatorio con máximo 100 caracteres.
    /// </summary>
    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Descripción opcional de la categoría.
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Indica si la categoría debe estar activa al crearse.
    /// Si no se especifica, por defecto es true.
    /// </summary>
    public bool IsActive { get; set; } = true;
}