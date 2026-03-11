namespace ProductsCrud.Models;

public abstract class Resource
{
    public List<LinkDto> Links { get; set; } = new List<LinkDto>();
}
