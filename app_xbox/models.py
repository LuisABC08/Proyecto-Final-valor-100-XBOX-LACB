from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# ===============================
#            CLIENTE
# ===============================

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# ===============================
#            VIDEOJUEGOS
# ===============================

class Videojuego(models.Model):
    ID_videojuego = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    desarrollador = models.CharField(max_length=255)
    genero = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()
    proveedor = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='videojuegos/', null=True, blank=True)

    def __str__(self):
        return self.nombre


# ===============================
#            CONSOLAS
# ===============================

class Consola(models.Model):
    ID_consola = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_lanzamiento = models.DateField()
    resolucion = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    almacenar_tipo = models.CharField(max_length=50)
    almacenar_espacio = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='consolas/', null=True, blank=True)

    def __str__(self):
        return self.nombre


# ===============================
#            ACCESORIOS
# ===============================

class Accesorio(models.Model):
    ID_accesorio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    compatibilidad = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='accesorios/', null=True, blank=True)

    def __str__(self):
        return self.nombre


# ===============================
#            PEDIDO
# ===============================

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente (Carrito)'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.user.username}"

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save()
        return self.total


# ===============================
#            PEDIDO ITEM
# ===============================

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"
    

# ===============================
#      NUEVO: DATOS GUARDADOS
# ===============================

class DireccionEnvio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    calle = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.calle}, {self.ciudad}"

class TarjetaGuardada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_titular = models.CharField(max_length=100)
    # En la vida real esto se encripta, para la escuela lo guardamos normal
    numero_tarjeta = models.CharField(max_length=16) 
    expiracion = models.CharField(max_length=5) # MM/YY
    cvv = models.CharField(max_length=4)

    def __str__(self):
        # Muestra solo los últimos 4 dígitos (Ej: Visa terminada en 4242)
        return f"Tarjeta terminada en {self.numero_tarjeta[-4:]}"