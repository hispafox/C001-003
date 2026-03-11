// =============================================================================
// Archivo      : CategoryUpdateDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO para la actualización de una categoría existente.
//                Todos los campos son opcionales para permitir actualizaciones parciales.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// DTO utilizado para actualizar una categoría existente.
/// Los campos son opcionales para permitir actualizaciones parciales.
/// </summary>
public class CategoryUpdateDto
{
    /// <summary>
    /// Nombre de la categoría. Opcional, máximo 100 caracteres.
    /// </summary>
    [MaxLength(100)]
    public string? Name { get; set; }

    /// <summary>
    /// Descripción opcional de la categoría.
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Indica si la categoría debe estar activa.
    /// Opcional para permitir actualizaciones selectivas.
    /// </summary>
    public bool? IsActive { get; set; }
}