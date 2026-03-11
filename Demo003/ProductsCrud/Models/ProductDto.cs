namespace ProductsCrud.Models;

public class ProductDto : Resource
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }

    /// <summary>
    /// Identificador del cliente que registró el producto.
    /// </summary>
    public int ClienteId { get; set; }

    /// <summary>
    /// Nombre completo del cliente que registró el producto (Nombre + Apellidos).
    /// </summary>
    public string ClienteNombre { get; set; } = string.Empty;

    /// <summary>
    /// Crea un <see cref="ProductDto"/> a partir de una entidad <see cref="Product"/>.
    /// La propiedad de navegación <c>Cliente</c> debe estar cargada para incluir el nombre.
    /// </summary>
    /// <param name="product">Entidad producto con su cliente cargado.</param>
    /// <returns>DTO con los datos del producto y el nombre del cliente.</returns>
    public static ProductDto FromProduct(Product product)
    {
        return new ProductDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price,
            Stock = product.Stock,
            ClienteId = product.ClienteId,
            ClienteNombre = product.Cliente is not null
                ? $"{product.Cliente.Nombre} {product.Cliente.Apellidos}"
                : string.Empty
        };
    }
}
