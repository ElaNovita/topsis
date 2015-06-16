from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import topsis
from .models import Pegawai, Kriteria, Penilaian


@login_required
def home(req):
    return render(req, 'home.html')


@login_required
def pegawai(req):
    pegawais = Pegawai.objects.all()
    return render(req, 'pegawai/all.html', {'pegawais': pegawais})


@login_required
def tambah_pegawai(req):
    kriterias = Kriteria.objects.all().order_by('id')
    if req.POST:
        nik = req.POST['nik']
        nama = req.POST['nama']
        jk = req.POST['jk']
        alamat = req.POST['alamat']
        kriteria_values = req.POST.getlist('kriteria')
        print kriteria_values
        try:
            p = Pegawai(nik=nik, nama=nama, jk=jk, alamat=alamat)
            p.save()

            # for k in kriteria_values:
            #     x = k.split('-')
            #     print x,
            #     kr = Kriteria.objects.get(id=x[0])
            #     nilai = Penilaian(pegawai=p, kriteria=kr, nilai=x[1])
            #     nilai.save()
            for k, v in zip(kriterias, kriteria_values):
                nilai = Penilaian(pegawai=p,
                                  kriteria=k,
                                  nilai=topsis.check_rules(int(v)),
                                  number=int(v))
                nilai.save()

            msg = {"status": "success", "msg": "Tersimpan !"}
        except Exception, e:
            print e
            msg = {"status": "danger", "msg": "Gagal !"}

    return render(req, 'pegawai/new.html', locals())


@login_required
def edit_pegawai(req, id):
    return render(req, 'pegawai/edit.html')


@login_required
def kriteria(req):
    kriterias = Kriteria.objects.all()
    return render(req, 'kriteria/all.html', {'kriterias': kriterias})


@login_required
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


@login_required
def penilaian(req):
    kriterias = Kriteria.objects.all()
    pegawais = Pegawai.objects.all().order_by('id')

    bobot = kriterias.values_list('bobot', flat=True)
    rules = kriterias.values_list('type', flat=True)

    data_mentah = OrderedDict()
    for i in pegawais:
        data_mentah[i.nama] = i.numbers()

    d = OrderedDict()
    for i in pegawais:
        d[i.nama] = i.matriks_d()

    matriks_d = []
    for i in d:
        matriks_d.append(d[i])

    r = OrderedDict()
    matriks_r = topsis.transform_to_r(matriks_d)
    for p, k in zip(pegawais, matriks_r):
        r[p.nama] = k

    v = OrderedDict()
    matriks_v = topsis.transform_to_v(matriks_r, bobot)
    for p, k in zip(pegawais, matriks_v):
        v[p.nama] = k

    solusi_ideal = topsis.A(matriks_v, rules)
    jarak_alternatif = topsis.S(matriks_v, solusi_ideal)
    jarak_tuple = zip(pegawais,
                      jarak_alternatif['positive'],
                      jarak_alternatif['negative'])

    preferensi_user = []
    preferensi = topsis.C(jarak_alternatif)
    for i in zip(pegawais, preferensi):
        preferensi_user.append([i[0].nama, i[1]])
    preferensi_user = sorted(preferensi_user, key=lambda x: x[1], reverse=True)

    return render(req, 'penilaian.html', locals())


def user_login(req):
    if req.POST:
        username = req.POST['username']
        password = req.POST['password']
        try:
            user = authenticate(username=username, password=password)
            login(req, user)
            return HttpResponseRedirect('/')
        except:
            return HttpResponseRedirect('/login')

    return render(req, 'login.html', locals())


def user_logout(req):
    logout(req)
    return HttpResponseRedirect('/login')
