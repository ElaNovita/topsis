# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama', models.CharField(max_length=50)),
                ('type', models.IntegerField(choices=[(1, b'Cost'), (2, b'Benefit')])),
                ('bobot', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nik', models.CharField(unique=True, max_length=10)),
                ('nama', models.CharField(max_length=50)),
                ('alamat', models.TextField()),
                ('jk', models.CharField(max_length=1, choices=[(b'l', b'Laki-laki'), (b'p', b'Perempuan')])),
            ],
        ),
        migrations.CreateModel(
            name='Penilaian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nilai', models.IntegerField()),
                ('kriteria', models.ForeignKey(to='core.Kriteria')),
                ('pegawai', models.ForeignKey(to='core.Pegawai')),
            ],
        ),
    ]
