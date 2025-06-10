from django.db import models

class estados (models.Model):

    id_estado= models.AutoField(primary_key=True)
    estado = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_estados'

    def __str__(self):
        return (self.estado)


class perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    perfil = models.CharField(max_length=1000)
    class Meta:
        db_table = 'rd_perfiles' 

    def __str__(self):
        return (self.perfil)

class usuario(models.Model):
    id_usuario=models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(perfil, on_delete=models.CASCADE, db_column='id_perfil')
    documento =models.CharField(max_length=15)
    nombre =models.CharField(max_length=50)
    usuario =models.CharField(max_length=15)
    clave =models.CharField(max_length=15)
    estado =models.CharField(max_length=15)
    class Meta:
        db_table = 'rd_usuarios'

    def __str__(self):
        return (self.usuario) 