// =============================================================================
// Archivo      : Product.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Modelo de dominio que representa un producto en el catálogo.
//                Incluye validaciones de datos mediante Data Annotations.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// Representa un producto del catálogo de la tienda.
/// </summary>
public class Product
{
    /// <summary>
    /// Identificador único del producto (clave primaria).
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre del producto. Requerido, máximo 200 caracteres.
    /// </summary>
    [Required]
    [MaxLength(200)]
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Descripción detallada del producto. Opcional, máximo 1000 caracteres.
    /// </summary>
    [MaxLength(1000)]
    public string? Description { get; set; }

    /// <summary>
    /// Precio unitario del producto. Debe ser mayor o igual a cero.
    /// </summary>
    [Range(0, double.MaxValue)]
    public decimal Price { get; set; }

    /// <summary>
    /// Cantidad disponible en inventario. Debe ser mayor o igual a cero.
    /// </summary>
    [Range(0, int.MaxValue)]
    public int Stock { get; set; }

    /// <summary>
    /// Identificador de la categoría a la que pertenece el producto (clave foránea obligatoria).
    /// </summary>
    [Required]
    public int CategoryId { get; set; }

    /// <summary>
    /// Categoría a la que pertenece el producto.
    /// Propiedad de navegación para acceder a los datos de la categoría.
    /// </summary>
    public Category? Category { get; set; }

    /// <summary>
    /// Identificador del cliente que registró el producto (clave foránea obligatoria).
    /// Todo producto debe estar asociado a un cliente.
    /// </summary>
    [Required]
    public int ClienteId { get; set; }

    /// <summary>
    /// Cliente que registró el producto.
    /// Propiedad de navegación para acceder a los datos del cliente.
    /// </summary>
    public Cliente? Cliente { get; set; }
}
