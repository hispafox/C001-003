// =============================================================================
// Archivo      : Category.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Modelo de dominio que representa una categoría de productos.
//                Incluye validaciones de datos mediante Data Annotations.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// Representa una categoría en la que se clasifican los productos.
/// Una categoría puede tener múltiples productos asociados.
/// </summary>
public class Category
{
    /// <summary>
    /// Identificador único de la categoría (clave primaria, autoincremental).
    /// </summary>
    public int Id { get; set; }

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
    /// Indica si la categoría está activa y puede ser utilizada.
    /// Por defecto es true.
    /// </summary>
    public bool IsActive { get; set; } = true;

    /// <summary>
    /// Colección de productos que pertenecen a esta categoría.
    /// Propiedad de navegación inversa para la relación 1:N.
    /// </summary>
    public ICollection<Product> Products { get; set; } = new List<Product>();
}