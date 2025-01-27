from django.db import models

class Sucursal(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    id_producto = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, related_name='productos', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} - {self.sucursal.nombre}'

    def reducir_stock(self, cantidad_vendida):
        """Reduce el stock de un producto después de realizar una venta."""
        if self.cantidad >= cantidad_vendida:
            self.cantidad -= cantidad_vendida
            self.save()
        else:
            raise ValueError("No hay suficiente stock para realizar la venta.")

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Venta {self.id} - {self.cliente.nombre} - {self.fecha}'
