from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.related import OneToOneField

# Create your models here.
class Sekolah(models.Model):
    sekolah_id = models.CharField(max_length=255, primary_key=True)
    siap_id = models.CharField(max_length=255)
    nama = models.CharField(max_length=255)
    npsn = models.CharField(max_length=255)
    is_negri = models.BooleanField(default=True)
    is_sbi = models.BooleanField(default=False)
    k_kota = models.CharField(max_length=255)
    k_propinsi = models.CharField(max_length=255)
    kota = models.CharField(max_length=255)
    propinsi = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)

class Siswa(models.Model):
    nilai = models.JSONField()
    siswa_id = models.CharField(max_length=255, primary_key=True)
    jalur = models.CharField(max_length=255)
    nilai_total = models.CharField(max_length=10)
    acc = models.CharField(max_length=255)
    pilihan1 = models.CharField(max_length=255)
    pilihan2 = models.CharField(max_length=255, null=True)
    pilihan3 = models.CharField(max_length=255, null=True)
    pilihanPenjurusan = models.JSONField(default=dict)
    year = models.CharField(max_length=5)
    zonasi = models.CharField(max_length=50, null=True, default=None)

class Ringkasan(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    rata2 = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    year = models.CharField(max_length=5)
    sum_type = models.CharField(max_length=50, default='all')

class Prediksi(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    prediksi = models.FloatField()


