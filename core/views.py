from django.shortcuts import render
from .topsis import *

from .models import Pegawai, Kriteria, Penilaian


def home(req):
    return render(req, 'home.html')


def pegawai(req):
    pegawais = Pegawai.objects.all()
    return render(req, 'pegawai/all.html', {'pegawais': pegawais})


def tambah_pegawai(req):
    if req.POST:
        nik = req.POST['nik']
        nama = req.POST['nama']
        jk = req.POST['jk']
        alamat = req.POST['alamat']
        kriterias = req.POST.getlist('kriteria')
        print kriterias
        try:
            p = Pegawai(nik=nik, nama=nama, jk=jk, alamat=alamat)
            p.save()

            for k in kriterias:
                x = k.split('-')
                print x,
                kr = Kriteria.objects.get(id=x[0])
                nilai = Penilaian(pegawai=p, kriteria=kr, nilai=x[1])
                nilai.save()

            msg = {"status": "success", "msg": "Tersimpan !"}
        except Exception, e:
            print e
            msg = {"status": "danger", "msg": "Gagal !"}

    kriterias = Kriteria.objects.all()
    return render(req, 'pegawai/new.html', locals())


def edit_pegawai(req, id):
    return render(req, 'pegawai/edit.html')


def kriteria(req):
    kriterias = Kriteria.objects.all()
    return render(req, 'kriteria/all.html', {'kriterias': kriterias})


def tambah_kriteria(req):
    if req.POST:
        nama = req.POST['nama']
        type = req.POST['type']
        bobot = req.POST['bobot']
        try:
            k = Kriteria(nama=nama, type=type, bobot=bobot)
            k.save()
            msg = {"status": "success", "msg": "Tersimpan !"}
        except Exception, e:
            print e
            msg = {"status": "danger", "msg": "Gagal !"}

    return render(req, 'kriteria/new.html', locals())


def penilaian(req):
    data = Penilaian.objects.all()
    return render(req, 'penilaian.html')