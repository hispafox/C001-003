using Microsoft.EntityFrameworkCore;
using ProductsCrud.Models;

namespace ProductsCrud.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    /// <summary>
    /// Conjunto de datos para la entidad Cliente.
    /// Permite realizar operaciones CRUD sobre los clientes del sistema.
    /// </summary>
    public DbSet<Cliente> Clientes => Set<Cliente>();

    /// <summary>
    /// Conjunto de datos para la entidad Usuario.
    /// Permite realizar operaciones CRUD sobre los usuarios del sistema (autenticación).
    /// </summary>
    public DbSet<Usuario> Usuarios => Set<Usuario>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configurar la relación 1:N entre Category y Product
        // Cada producto debe tener una categoría obligatoria
        modelBuilder.Entity<Product>()
            .HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .IsRequired()
            .OnDelete(DeleteBehavior.Restrict);

        // Configurar la relación 1:N entre Cliente y Product
        // Cada producto debe estar asociado a un cliente (el que lo registró)
        modelBuilder.Entity<Product>()
            .HasOne(p => p.Cliente)
            .WithMany(c => c.Productos)
            .HasForeignKey(p => p.ClienteId)
            .IsRequired()
            .OnDelete(DeleteBehavior.Restrict);

        // Configurar índice único en el email del cliente
        // Garantiza que no puedan existir dos clientes con el mismo correo
        modelBuilder.Entity<Cliente>()
            .HasIndex(c => c.Email)
            .IsUnique();

        // =====================================================================
        // Configuración de la entidad Usuario
        // =====================================================================

        // Configurar índice único en NombreUsuario
        // Garantiza que no puedan existir dos usuarios con el mismo nombre
        modelBuilder.Entity<Usuario>()
            .HasIndex(u => u.NombreUsuario)
            .IsUnique();

        // Configurar índice único en Email
        // Garantiza que no puedan existir dos usuarios con el mismo correo
        modelBuilder.Entity<Usuario>()
            .HasIndex(u => u.Email)
            .IsUnique();

        // Seed: usuario administrador por defecto
        // La contraseña "Admin123!" se almacena hasheada con BCrypt
        // Se usa un hash pre-calculado para evitar que EF Core detecte valores dinámicos
        modelBuilder.Entity<Usuario>().HasData(
            new Usuario
            {
                Id = 1,
                NombreUsuario = "admin",
                Email = "admin@productscrud.com",
                PasswordHash = "$2a$11$pnd2xM8ZyIXv94DB2Xjwh.WMAx2clNoYOG4HC0N/g5Mbzxow5pEqW",
                Rol = "Admin",
                FechaCreacion = new DateTime(2026, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                Activo = true
            }
        );
    }
}
