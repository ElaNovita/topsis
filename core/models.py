from django.db import models

JK_CHOICES = (
    ('l', 'Laki-laki'),
    ('p', 'Perempuan')
)


class Pegawai(models.Model):
    nik = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50)
    alamat = models.TextField()
    jk = models.CharField(choices=JK_CHOICES, max_length=1)

    def __unicode__(self):
        return self.nama


class Kandidat(models.Model):
    pegawai = models.OneToOneField(Pegawai)

    def __unicode__(self):
        return self.pegawai.nama


class Kriteria(models.Model):
    nama = models.CharField(max_length=50)
    