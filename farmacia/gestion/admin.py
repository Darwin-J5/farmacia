from django.contrib import admin

from gestion.models import Sucursal, Producto, Cliente


# Register your models here.
@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'telefono')
    list_filter = ('direccion',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'cantidad', 'precio', 'sucursal')
    search_fields = ('id_producto', 'nombre', 'precio')
    list_filter = ('id_producto',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
