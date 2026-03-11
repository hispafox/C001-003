// =============================================================================
// Archivo      : ClienteUpdateDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO para la actualización de un cliente existente.
//                Todos los campos son opcionales para permitir actualizaciones
//                parciales del recurso.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// DTO utilizado para actualizar un cliente existente.
/// Los campos son opcionales para permitir actualizaciones parciales.
/// Solo se modificarán los campos que se envíen en la petición.
/// </summary>
public class ClienteUpdateDto
{
    /// <summary>
    /// Nombre del cliente. Opcional, máximo 100 caracteres.
    /// </summary>
    [MaxLength(100)]
    public string? Nombre { get; set; }

    /// <summary>
    /// Apellidos del cliente. Opcional, máximo 150 caracteres.
    /// </summary>
    [MaxLength(150)]
    public string? Apellidos { get; set; }

    /// <summary>
    /// Correo electrónico del cliente. Opcional, debe tener formato válido.
    /// Máximo 255 caracteres. Debe ser único en el sistema.
    /// </summary>
    [MaxLength(255)]
    [EmailAddress]
    public string? Email { get; set; }

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
    /// Indica si el cliente debe estar activo.
    /// Opcional para permitir actualizaciones selectivas.
    /// </summary>
    public bool? Activo { get; set; }
}
