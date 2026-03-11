// =============================================================================
// Archivo      : Cliente.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Modelo de dominio que representa un cliente del sistema.
//                Cada cliente puede tener múltiples productos asociados
//                (relación 1:N obligatoria). Incluye validaciones de datos
//                mediante Data Annotations.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// Representa un cliente registrado en el sistema.
/// Un cliente puede tener múltiples productos asociados (los que registró).
/// Relación 1:N obligatoria: cada producto debe pertenecer a un cliente.
/// </summary>
public class Cliente
{
    /// <summary>
    /// Identificador único del cliente (clave primaria, autoincremental).
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre del cliente. Campo obligatorio con máximo 100 caracteres.
    /// </summary>
    [Required]
    [MaxLength(100)]
    public string Nombre { get; set; } = string.Empty;

    /// <summary>
    /// Apellidos del cliente. Campo obligatorio con máximo 150 caracteres.
    /// </summary>
    [Required]
    [MaxLength(150)]
    public string Apellidos { get; set; } = string.Empty;

    /// <summary>
    /// Correo electrónico del cliente. Obligatorio, único en el sistema y con formato válido.
    /// Máximo 255 caracteres. El índice único se configura en AppDbContext.
    /// </summary>
    [Required]
    [MaxLength(255)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    /// <summary>
    /// Número de teléfono del cliente. Opcional, máximo 20 caracteres.
    /// </summary>
    [MaxLength(20)]
    public string? Telefono { get; set; }

    /// <summary>
    /// Dirección del cliente. Opcional, máximo 300 caracteres.
    /// </summary>
    [MaxLength(300)]
    public string? Direccion { get; set; }

    /// <summary>
    /// Fecha en que el cliente fue dado de alta en el sistema.
    /// Se asigna automáticamente con la fecha y hora actual al crear el registro.
    /// </summary>
    public DateTime FechaAlta { get; set; } = DateTime.Now;

    /// <summary>
    /// Indica si el cliente está activo en el sistema.
    /// Por defecto es <c>true</c>. Se usa para soft delete (borrado lógico).
    /// </summary>
    public bool Activo { get; set; } = true;

    /// <summary>
    /// Colección de productos registrados por este cliente.
    /// Propiedad de navegación inversa para la relación 1:N (Cliente → Productos).
    /// </summary>
    public ICollection<Product> Productos { get; set; } = new List<Product>();
}
