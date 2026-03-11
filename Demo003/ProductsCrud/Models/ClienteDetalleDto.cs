// =============================================================================
// Archivo      : ClienteDetalleDto.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : DTO detallado para representar un cliente con sus productos.
//                Incluye toda la información del cliente y la lista completa
//                de productos asociados con sus respectivas categorías.
// =============================================================================

namespace ProductsCrud.Models;

/// <summary>
/// DTO detallado utilizado para mostrar un cliente con toda su información
/// y la lista completa de productos asociados, incluyendo la categoría de cada uno.
/// Se usa en el endpoint GET api/clientes/{id}.
/// </summary>
public class ClienteDetalleDto
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
    /// Dirección del cliente.
    /// </summary>
    public string? Direccion { get; set; }

    /// <summary>
    /// Fecha en que el cliente fue dado de alta en el sistema.
    /// </summary>
    public DateTime FechaAlta { get; set; }

    /// <summary>
    /// Indica si el cliente está activo en el sistema.
    /// </summary>
    public bool Activo { get; set; }

    /// <summary>
    /// Lista de productos asociados a este cliente.
    /// Cada producto incluye información resumida y el nombre de su categoría.
    /// </summary>
    public List<ClienteProductoDto> Productos { get; set; } = new List<ClienteProductoDto>();
}

/// <summary>
/// DTO resumido para representar un producto en el contexto de un cliente.
/// Incluye información básica del producto y el nombre de su categoría.
/// </summary>
public class ClienteProductoDto
{
    /// <summary>
    /// Identificador único del producto.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre del producto.
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Precio del producto.
    /// </summary>
    public decimal Price { get; set; }

    /// <summary>
    /// Nombre de la categoría a la que pertenece el producto.
    /// </summary>
    public string CategoryName { get; set; } = string.Empty;
}
