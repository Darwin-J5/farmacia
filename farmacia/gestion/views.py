from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, Producto, Cliente, Venta
from django.contrib import messages


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')


def inventario(request):
    sucursales = Sucursal.objects.all()
    sucursal_id = request.GET.get('sucursal')
    productos = Producto.objects.none()  # Iniciar con una lista vacía de productos

    if sucursal_id:
        productos = Producto.objects.filter(sucursal_id=sucursal_id)

    return render(request, 'inventario.html', {'sucursales': sucursales, 'productos': productos})

def venta(request):
    sucursales = Sucursal.objects.all()
    productos = Producto.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        sucursal_id = request.POST.get('sucursal')
        productos_seleccionados = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')

        cliente = get_object_or_404(Cliente, id=cliente_id)
        sucursal = get_object_or_404(Sucursal, id=sucursal_id)

        # Crear la venta
        venta = Venta(cliente=cliente, sucursal=sucursal)
        venta.save()

        total = 0
        for prod_id, cantidad in zip(productos_seleccionados, cantidades):
            cantidad = int(cantidad)
            producto = get_object_or_404(Producto, id=prod_id, sucursal=sucursal)

            # Verificar que haya suficiente stock
            if producto.cantidad >= cantidad:
                producto.reducir_stock(cantidad)  # Reducir stock
                total += producto.precio * cantidad
            else:
                messages.error(request, f"No hay suficiente stock de {producto.nombre}.")
                return redirect('venta')  # Redirigir si no hay suficiente stock

        # Actualizar el total de la venta
        venta.total = total
        venta.save()

        messages.success(request, f'Venta realizada con éxito. Total: ${total}')
        return redirect('venta')  # Redirigir después de completar la venta

    return render(request, 'venta.html', {
        'sucursales': sucursales,
        'productos': productos,
        'clientes': clientes,
    })
