using System.ComponentModel.DataAnnotations;

namespace Demo002.Models;

public class Product
{
    public int Id { get; set; }

    [Required(ErrorMessage = "El nombre es obligatorio")]
    [StringLength(120)]
    [Display(Name = "Nombre")]
    public string Name { get; set; } = string.Empty;

    [StringLength(400)]
    [Display(Name = "Descripcion")]
    public string? Description { get; set; }

    [Range(0, 999999.99)]
    [Display(Name = "Precio")]
    public decimal Price { get; set; }

    [Range(0, int.MaxValue)]
    [Display(Name = "Stock")]
    public int Stock { get; set; }

    [Display(Name = "Fecha de creacion")]
    [DataType(DataType.Date)]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
