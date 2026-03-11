// =============================================================================
// Archivo      : ClientesController.cs
// Autor        : Equipo de Desarrollo
// Versión      : 1.0.0
// Fecha        : 2026-03-10
// Descripción  : Controlador REST que expone los endpoints CRUD para la entidad
//                Cliente. Utiliza Entity Framework Core para el acceso a datos.
//                Incluye filtros por estado activo y búsqueda por texto.
// =============================================================================

using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProductsCrud.Data;
using ProductsCrud.Models;

namespace ProductsCrud.Controllers;

/// <summary>
/// Controlador de la API para la gestión de clientes.
/// Expone operaciones CRUD sobre el recurso <see cref="Cliente"/>.
/// Ruta base: <c>api/clientes</c>.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ClientesController(AppDbContext db) : ControllerBase
{
    /// <summary>
    /// Obtiene la lista de clientes con filtros opcionales.
    /// </summary>
    /// <param name="activo">Si se especifica, filtra los clientes por estado activo/inactivo.</param>
    /// <param name="buscar">
    /// Texto de búsqueda. Filtra clientes cuyo Nombre, Apellidos o Email
    /// contengan el texto indicado (búsqueda parcial, sin distinción de mayúsculas).
    /// </param>
    /// <returns>Lista de clientes en formato resumido con el conteo de productos.</returns>
    /// <response code="200">Retorna la lista de clientes.</response>
    [HttpGet]
    [ProducesResponseType(typeof(List<ClienteResumenDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll([FromQuery] bool? activo, [FromQuery] string? buscar)
    {
        var query = db.Clientes.AsQueryable();

        // Filtrar por estado activo si se especifica el parámetro
        if (activo.HasValue)
        {
            query = query.Where(c => c.Activo == activo.Value);
        }

        // Filtrar por texto de búsqueda en Nombre, Apellidos y Email
        if (!string.IsNullOrWhiteSpace(buscar))
        {
            var terminoBusqueda = buscar.Trim().ToLower();
            query = query.Where(c =>
                c.Nombre.ToLower().Contains(terminoBusqueda) ||
                c.Apellidos.ToLower().Contains(terminoBusqueda) ||
                c.Email.ToLower().Contains(terminoBusqueda));
        }

        var clientes = await query
            .Select(c => new ClienteResumenDto
            {
                Id = c.Id,
                Nombre = c.Nombre,
                Apellidos = c.Apellidos,
                Email = c.Email,
                Telefono = c.Telefono,
                Activo = c.Activo,
                FechaAlta = c.FechaAlta,
                ProductosCount = c.Productos.Count
            })
            .ToListAsync();

        return Ok(clientes);
    }

    /// <summary>
    /// Obtiene un cliente por su identificador único con información detallada.
    /// Incluye la lista completa de productos asociados con sus categorías.
    /// </summary>
    /// <param name="id">Identificador del cliente.</param>
    /// <returns>El cliente con toda su información y sus productos asociados.</returns>
    /// <response code="200">Retorna el cliente encontrado con sus productos.</response>
    /// <response code="404">No existe un cliente con el id indicado.</response>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(ClienteDetalleDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(int id)
    {
        // Incluir productos y sus categorías para el DTO de detalle
        var cliente = await db.Clientes
            .Include(c => c.Productos)
                .ThenInclude(p => p.Category)
            .FirstOrDefaultAsync(c => c.Id == id);

        if (cliente is null)
        {
            return NotFound(new ProblemDetails
            {
                Status = 404,
                Title = "Cliente no encontrado.",
                Detail = $"El cliente con Id {id} no existe."
            });
        }

        var dto = new ClienteDetalleDto
        {
            Id = cliente.Id,
            Nombre = cliente.Nombre,
            Apellidos = cliente.Apellidos,
            Email = cliente.Email,
            Telefono = cliente.Telefono,
            Direccion = cliente.Direccion,
            FechaAlta = cliente.FechaAlta,
            Activo = cliente.Activo,
            Productos = cliente.Productos.Select(p => new ClienteProductoDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price,
                CategoryName = p.Category?.Name ?? string.Empty
            }).ToList()
        };

        return Ok(dto);
    }

    /// <summary>
    /// Crea un nuevo cliente en el sistema.
    /// Valida que el email no esté registrado previamente.
    /// </summary>
    /// <param name="dto">Datos del cliente a registrar.</param>
    /// <returns>El cliente recién creado con su identificador asignado.</returns>
    /// <response code="201">Cliente creado exitosamente.</response>
    /// <response code="400">Datos no válidos o email duplicado.</response>
    [HttpPost]
    [ProducesResponseType(typeof(ClienteDetalleDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(ClienteCreateDto dto)
    {
        // Validar que el email no esté ya registrado en el sistema
        var emailExiste = await db.Clientes.AnyAsync(c => c.Email == dto.Email);
        if (emailExiste)
        {
            return BadRequest(new ProblemDetails
            {
                Status = 400,
                Title = "Email duplicado.",
                Detail = $"Ya existe un cliente registrado con el email '{dto.Email}'."
            });
        }

        // Mapear del DTO a la entidad
        var cliente = new Cliente
        {
            Nombre = dto.Nombre,
            Apellidos = dto.Apellidos,
            Email = dto.Email,
            Telefono = dto.Telefono,
            Direccion = dto.Direccion
        };

        db.Clientes.Add(cliente);
        await db.SaveChangesAsync();

        // Construir el DTO de respuesta (sin productos, ya que es un cliente nuevo)
        var resultDto = new ClienteDetalleDto
        {
            Id = cliente.Id,
            Nombre = cliente.Nombre,
            Apellidos = cliente.Apellidos,
            Email = cliente.Email,
            Telefono = cliente.Telefono,
            Direccion = cliente.Direccion,
            FechaAlta = cliente.FechaAlta,
            Activo = cliente.Activo,
            Productos = new List<ClienteProductoDto>()
        };

        return CreatedAtAction(nameof(GetById), new { id = cliente.Id }, resultDto);
    }

    /// <summary>
    /// Actualiza un cliente existente.
    /// Solo se modifican los campos que se envíen en la petición.
    /// Valida que el email no esté en uso por otro cliente.
    /// </summary>
    /// <param name="id">Identificador del cliente a actualizar.</param>
    /// <param name="dto">Datos actualizados del cliente.</param>
    /// <returns>Sin contenido si la operación fue exitosa.</returns>
    /// <response code="204">Cliente actualizado correctamente.</response>
    /// <response code="400">Datos no válidos o email duplicado.</response>
    /// <response code="404">No existe un cliente con el id indicado.</response>
    [HttpPut("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(int id, ClienteUpdateDto dto)
    {
        var cliente = await db.Clientes.FindAsync(id);
        if (cliente is null)
        {
            return NotFound(new ProblemDetails
            {
                Status = 404,
                Title = "Cliente no encontrado.",
                Detail = $"El cliente con Id {id} no existe."
            });
        }

        // Validar email único excluyendo al propio cliente
        if (dto.Email is not null)
        {
            var emailExiste = await db.Clientes
                .AnyAsync(c => c.Email == dto.Email && c.Id != id);
            if (emailExiste)
            {
                return BadRequest(new ProblemDetails
                {
                    Status = 400,
                    Title = "Email duplicado.",
                    Detail = $"Ya existe otro cliente registrado con el email '{dto.Email}'."
                });
            }
        }

        // Actualizar solo los campos que se enviaron (actualización parcial)
        if (dto.Nombre is not null)
        {
            cliente.Nombre = dto.Nombre;
        }

        if (dto.Apellidos is not null)
        {
            cliente.Apellidos = dto.Apellidos;
        }

        if (dto.Email is not null)
        {
            cliente.Email = dto.Email;
        }

        if (dto.Telefono is not null)
        {
            cliente.Telefono = dto.Telefono;
        }

        if (dto.Direccion is not null)
        {
            cliente.Direccion = dto.Direccion;
        }

        if (dto.Activo.HasValue)
        {
            cliente.Activo = dto.Activo.Value;
        }

        await db.SaveChangesAsync();

        return NoContent();
    }

    /// <summary>
    /// Elimina un cliente del sistema (soft delete).
    /// Si el cliente tiene productos asociados, retorna Conflict (409).
    /// Si no tiene productos, lo marca como inactivo (borrado lógico).
    /// </summary>
    /// <param name="id">Identificador del cliente a eliminar.</param>
    /// <returns>Sin contenido si se eliminó correctamente.</returns>
    /// <response code="204">Cliente desactivado correctamente.</response>
    /// <response code="404">No existe un cliente con el id indicado.</response>
    /// <response code="409">No se puede eliminar porque tiene productos asociados.</response>
    [HttpDelete("{id}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> Delete(int id)
    {
        var cliente = await db.Clientes
            .Include(c => c.Productos)
            .FirstOrDefaultAsync(c => c.Id == id);

        if (cliente is null)
        {
            return NotFound(new ProblemDetails
            {
                Status = 404,
                Title = "Cliente no encontrado.",
                Detail = $"El cliente con Id {id} no existe."
            });
        }

        // Verificar si tiene productos asociados antes de eliminar
        if (cliente.Productos.Any())
        {
            return Conflict(new ProblemDetails
            {
                Status = 409,
                Title = "No se puede eliminar el cliente.",
                Detail = "El cliente tiene productos asociados y no puede ser eliminado."
            });
        }

        // Soft delete: marcar como inactivo en lugar de eliminar físicamente
        cliente.Activo = false;
        await db.SaveChangesAsync();

        return NoContent();
    }
}
