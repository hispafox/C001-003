// =============================================================================
// Archivo      : ClienteResumenDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO resumido para representar un cliente en listados.
//                Incluye el conteo de productos asociados sin listarlos.
// =============================================================================

namespace ProductsCrud.Models;

/// <summary>
/// DTO resumido utilizado para mostrar clientes en listados.
/// Incluye información básica y el número de productos asociados,
/// sin incluir el detalle de cada producto.
/// </summary>
public class ClienteResumenDto
{
    /// <summary>
    /// Identificador único del cliente.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre del cliente.
    /// </summary>
    public string Nombre { get; set; } = string.Empty;

    /// <summary>
    /// Apellidos del cliente.
    /// </summary>
    public string Apellidos { get; set; } = string.Empty;

    /// <summary>
    /// Correo electrónico del cliente.
    /// </summary>
    public string Email { get; set; } = string.Empty;

    /// <summary>
    /// Número de teléfono del cliente.
    /// </summary>
    public string? Telefono { get; set; }

    /// <summary>
    /// Indica si el cliente está activo en el sistema.
    /// </summary>
    public bool Activo { get; set; }

    /// <summary>
    /// Fecha en que el cliente fue dado de alta.
    /// </summary>
    public DateTime FechaAlta { get; set; }

    /// <summary>
    /// Número de productos asociados a este cliente.
    /// Se calcula a partir de la colección de productos, sin listarlos.
    /// </summary>
    public int ProductosCount { get; set; }
}
