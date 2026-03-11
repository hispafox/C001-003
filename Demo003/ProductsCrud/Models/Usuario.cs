// =============================================================================
// Archivo      : Usuario.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Modelo de dominio que representa un usuario del sistema.
//                Incluye validaciones de datos mediante Data Annotations.
//                Se utiliza para autenticación y autorización con JWT.
// =============================================================================

using System.ComponentModel.DataAnnotations;

namespace ProductsCrud.Models;

/// <summary>
/// Representa un usuario registrado en el sistema.
/// Contiene las credenciales y datos necesarios para autenticación y autorización.
/// </summary>
public class Usuario
{
    /// <summary>
    /// Identificador único del usuario (clave primaria, autoincremental).
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Nombre de usuario. Campo obligatorio, único en el sistema y con máximo 50 caracteres.
    /// El índice único se configura en AppDbContext.
    /// </summary>
    [Required]
    [MaxLength(50)]
    public string NombreUsuario { get; set; } = string.Empty;

    /// <summary>
    /// Correo electrónico del usuario. Obligatorio, único en el sistema y con formato válido.
    /// Máximo 255 caracteres. El índice único se configura en AppDbContext.
    /// </summary>
    [Required]
    [MaxLength(255)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    /// <summary>
    /// Hash de la contraseña del usuario generado con BCrypt.
    /// Nunca se almacena la contraseña en texto plano.
    /// </summary>
    [Required]
    public string PasswordHash { get; set; } = string.Empty;

    /// <summary>
    /// Rol del usuario en el sistema. Valores permitidos: "Admin" o "Usuario".
    /// Por defecto se asigna el rol "Usuario".
    /// </summary>
    [Required]
    [MaxLength(20)]
    public string Rol { get; set; } = "Usuario";

    /// <summary>
    /// Fecha y hora en que se creó el registro del usuario.
    /// Se asigna automáticamente al momento de la creación.
    /// </summary>
    public DateTime FechaCreacion { get; set; } = DateTime.Now;

    /// <summary>
    /// Indica si el usuario está activo en el sistema.
    /// Un usuario inactivo no puede iniciar sesión. Por defecto es true.
    /// </summary>
    public bool Activo { get; set; } = true;
}
