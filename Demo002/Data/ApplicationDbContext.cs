using Demo002.Models;
using Microsoft.EntityFrameworkCore;

namespace Demo002.Data;

public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products => Set<Product>();
}
