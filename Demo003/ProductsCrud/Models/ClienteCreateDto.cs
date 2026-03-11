// =============================================================================
// Archivo      : ClienteCreateDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO para la creación de un nuevo cliente.
//                Contiene solo los campos necesarios para registrar un cliente.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// DTO utilizado para crear un nuevo cliente en el sistema.
/// Incluye validaciones para asegurar la integridad de los datos.
/// </summary>
public class ClienteCreateDto
{
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
    /// Correo electrónico del cliente. Obligatorio, debe tener formato válido.
    /// Máximo 255 caracteres. Debe ser único en el sistema.
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
}
