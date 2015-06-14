from django.shortcuts import render


def home(req):
    return render(req, 'home.html')


def pegawai(req):
    return render(req, 'pegawai/all.html')


def tambah_pegawai(req):
    return render(req, 'pegawai/new.html')


def edit_pegawai(req, id):
    return render(req, 'pegawai/edit.html')