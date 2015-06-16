from django.db import models

JK_CHOICES = (
    ('l', 'Laki-laki'),
    ('p', 'Perempuan')
)
NILAI = (
    (1, "Kurang"),
    (2, "Cukup"),
    (3, "Baik"),
    (4, "Sangat Baik"),
)
TYPE = (
    (1, "Cost"),
    (2, "Benefit")
)
# BOBOT = []
# RULES = [1, 1, 1, 1, 1, 1]  # semua kriteria merupakan keuntungan


class Pegawai(models.Model):
    nik = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50)
    alamat = models.TextField()
    jk = models.CharField(choices=JK_CHOICES, max_length=1)

    def matriks_d(self):
        return self.nilai.values_list('nilai', flat=True)

    def numbers(self):
        return self.nilai.values_list('number', flat=True)

    def __unicode__(self):
        return self.nama


class Kriteria(models.Model):
    nama = models.CharField(max_length=50)
    type = models.IntegerField(choices=TYPE)
    bobot = models.IntegerField()

    def __unicode__(self):
        return self.nama


class Penilaian(models.Model):
    pegawai = models.ForeignKey(Pegawai, related_name='nilai')
    kriteria = models.ForeignKey(Kriteria)
    number = models.IntegerField()
    nilai = models.IntegerField()

    def __unicode__(self):
        return "%s: %s" % (self.pegawai.nama, self.nilai)
