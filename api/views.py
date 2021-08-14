from json.encoder import JSONEncoder
from api.models import Prediksi, Sekolah, Siswa, Ringkasan
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests as rq, json as js
from django.db.utils import IntegrityError
import csv

def endpoint(request):
    return HttpResponse('endpoint')

def sekolah(request):
    url = 'https://arsip.siap-ppdb.com/2019/yogyaprov/sekolah/1-sma-reguler.json'
    data_sekolah = rq.get(url).json()
    for data in data_sekolah:
        s = Sekolah()
        for k, v in data.items():
            setattr(s, k, v)
        s.save()

    return HttpResponse("hhh")

def siswa(request, year):
    sekolah_id = [data.sekolah_id for data in Sekolah.objects.all()]
    #sekolah_id = sekolah_id[17:]
    print(len(sekolah_id))
    itterCount = 70 - len(sekolah_id)
    if (year == 2020):
        for data in sekolah_id:
            url1 = rq.get(f'https://arsip.siap-ppdb.com/{year}/yogyaprov/seleksi/reguler/sma/1-{data}-1000.json').json()['data']
            print(f'Sekolah ke-{itterCount}')
            itterCount += 1
            #print(url1)
            #break
            for deeper in url1:
                s = Siswa()
                # siswa_id, nilai_total, jalur, zonasi
                #s.siswa_id = deeper[2]
                #print(f"\r\t Fetching {s.siswa_id}")
                s.nilai_total = str(float(deeper[-4])*4)
                s.year = year
                s.jalur = 'Jalur Zonasi' 
                if (s.jalur == 'Jalur Zonasi'):
                    s.zonasi = deeper[4]
                else:
                    s.zonasi = None
                headers = {'Accept': 'application/json, text/plain, */*',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Connection': 'keep-alive',
                            'Cookie': '_ga=GA1.2.808158056.1627785792',
                            'Host': 'arsip.siap-ppdb.com',
                            'Referer': f'https://arsip.siap-ppdb.com/{year}/yogyaprov/',
                            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                            'sec-ch-ua-mobile': '?0',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                            }
                headers18 = {'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Connection': 'keep-alive',
                    'Cookie': '_ga=GA1.2.808158056.1627785792; _gid=GA1.2.562046806.1627785792',
                    'Host': 'arsip.siap-ppdb.com',
                    'Referer': 'https://arsip.siap-ppdb.com/2018/yogyaprov/',
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'sec-ch-ua-mobile': '?0',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                    }
                # nilai, acc, pil 1, 2 , 3, jurusan
                while True:
                    try:
                        url2 = second_request = rq.get(f'https://arsip.siap-ppdb.com/{year}/api/cari?no_daftar={deeper[2]}', headers=headers).json()
                        #print(url2)
                        #break
                        s.siswa_id = url2[0][-1][1][-1]
                        #nilai UN
                        nilaiBase = url2[3][-1]
                        nilai_list = []
                        index = 0
                        for nilai in nilaiBase:
                            if (index > 3):
                                nilai_list.append(s.nilai_total)
                                break
                            nilai_list.append(nilai[-1][0])
                            index += 1
                        s.nilai = js.dumps(nilai_list)
                        
                        # acc
                        s.acc = url2[-1][-1][1][-2]
                        
                        # pilihan & jurusan
                        pilihanBase = url2[-2][-1]
                        pilihanJurusan = []
                        for i in range(3):
                            try:
                                usedBase = pilihanBase[i][-1]
                                setattr(s, f'pilihan{i+1}', usedBase[0][-1])
                                pilihanJurusan.append(usedBase[1][-2])
                            except IndexError:
                                setattr(s, f'pilihan{i+1}', None)
                                pilihanJurusan.append(None)
                        s.pilihanPenjurusan= js.dumps(pilihanJurusan)
                        try:
                            s.save()
                            print(f'\t{s.siswa_id} Fetch Complete', end='\r')
                        except IntegrityError:
                            print("INTEGRITY ERROR")
                    except ConnectionError:
                        print("CONECTION ERROR")
                    else:
                        break
                # break Development
    elif (year == 2021):
        iter = 1
        for data in sekolah_id:
            url1 = rq.get(f'https://ppdb.jogjaprov.go.id/seleksi/reguler/sma/1-{data}-1000.json', verify=False).json()['data']
            print(iter, end='\n')
            for deeper in url1:
                s = Siswa()
                s.zonasi = deeper[4]
                s.nilai_total = deeper[5]
                no_daftar = deeper[2]
                s.year = year

                headers2 = {'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Connection': 'keep-alive',
                    'Host': 'api.siap-ppdb.com',
                    'Origin': 'https://ppdb.jogjaprov.go.id',
                    'Referer': 'https://ppdb.jogjaprov.go.id/',
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'sec-ch-ua-mobile': '?0',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'cross-site',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
                    }

                while True:
                    try:
                        url2 = rq.get(f'https://api.siap-ppdb.com/cari?no_daftar={no_daftar}', headers=headers2).json()

                        s.siswa_id = url2[0][-1][1][-1]

                        nilai_base_aspd = url2[3][-1]
                        nilai_base_rapor = url2[4][-1]
                        
                        nilai_list = []

                        for i in range(4):
                            aspd = float(nilai_base_aspd[i][-1][0])
                            raport = float(nilai_base_rapor[i][-1][0])
                            nilai_list.append(str( (aspd + raport)/2 ) )

                        s.nilai = js.dumps(nilai_list)

                        s.acc = url2[-1][-1][1][-2]
                        pilihan_base = url2[-2][-1]
                        jurusan_list = []
                        for i in range(3):
                            try:
                                used_base = pilihan_base[i][-1]
                                setattr(s, f'pilihan{i+1}', used_base[0][-1])
                                jurusan_list.append(used_base[1][-2])
                            except IndexError:
                                setattr(s, f'pilihan{i+1}', None)
                                jurusan_list.append(None)

                        s.pilihanPenjurusan = js.dumps(jurusan_list)

                        try:
                            s.save()
                        except IntegrityError:
                            print("Intergrity Error")
                    except ConnectionError:
                        print("COnnection Error")
                    else:
                        break    

            iter += 1
    elif (year == 2018):
        iter = 1
        sekolah_id = sekolah_id[60:]
        iter = 70 - len(sekolah_id)
        for data in sekolah_id:
            url1 = rq.get(f'https://arsip.siap-ppdb.com/2018/yogyaprov/seleksi/reguler/sma/1-{data}-1000.json', verify=False).json()['data']
            print(iter, year, end='\n')
            for deeper in url1:
                s = Siswa()
                s.jalur = deeper[9]
                s.nilai_total = deeper[11]
                no_daftar = deeper[7]
                s.year = year
                if s.jalur == 'Jalur Zonasi':
                    s.zonasi = deeper[10]
                else:
                    s.zonasi = None
                

                headers18 = {'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Connection': 'keep-alive',
                    'Cookie': '_ga=GA1.2.808158056.1627785792; _gid=GA1.2.562046806.1627785792',
                    'Host': 'arsip.siap-ppdb.com',
                    'Referer': 'https://arsip.siap-ppdb.com/2018/yogyaprov/',
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'sec-ch-ua-mobile': '?0',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                    }

                while True:
                    try:
                        url2 = rq.get(f'https://arsip.siap-ppdb.com/2018/api/cari?no_daftar={no_daftar}', headers=headers18).json()

                        s.siswa_id = url2[0][-1][1][-1]

                        nilai_base = url2[2][-1]
                        
                        nilai_list = []

                        for nilai in nilai_base:
                            nilai_list.append(str(nilai[-1][0]))

                        s.nilai = js.dumps(nilai_list)

                        s.acc = url2[-1][-1][1][-2]
                        pilihan_base = url2[-2][-1]
                        jurusan_list = []
                        for i in range(3):
                            try:
                                used_base = pilihan_base[i][-1]
                                setattr(s, f'pilihan{i+1}', used_base[0][-1])
                                jurusan_list.append(used_base[1][-2])
                            except IndexError:
                                setattr(s, f'pilihan{i+1}', None)
                                jurusan_list.append(None)

                        s.pilihanPenjurusan = js.dumps(jurusan_list)

                        try:
                            s.save()
                        except IntegrityError:
                            print("Intergrity Error")
                    except ConnectionError:
                        print("COnnection Error")
                    
                    else:
                        break    

            iter += 1
                




    else:
        itterCount = 0
        for data in sekolah_id:
            url1 = rq.get(f'https://arsip.siap-ppdb.com/{year}/yogyaprov/seleksi/reguler/sma/1-{data}-0.json').json()['data']
            print(itterCount, year)
            itterCount += 1
            #print(url1)
            #break
            for deeper in url1:
                s = Siswa()
                # siswa_id, nilai_total, jalur, zonasi
                #s.siswa_id = deeper[4]
                s.nilai_total = deeper[6]
                s.year = year
                s.jalur = 'Jalur Reguler'
                s.zonasi = None
                headers = {'Accept': 'application/json, text/plain, */*',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Connection': 'keep-alive',
                            'Cookie': '_ga=GA1.2.808158056.1627785792; _gid=GA1.2.562046806.1627785792; _gat=1',
                            'Host': 'arsip.siap-ppdb.com',
                            'Referer': f'https://arsip.siap-ppdb.com/{year}/yogyaprov/',
                            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                            'sec-ch-ua-mobile': '?0',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                            }
                headers18 = {'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Connection': 'keep-alive',
                    'Cookie': '_ga=GA1.2.808158056.1627785792; _gid=GA1.2.562046806.1627785792',
                    'Host': 'arsip.siap-ppdb.com',
                    'Referer': 'https://arsip.siap-ppdb.com/2018/yogyaprov/',
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'sec-ch-ua-mobile': '?0',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                    }
                # nilai, acc, pil 1, 2 , 3, jurusan
                while True:
                    try:
                        url2 = second_request = rq.get(f'https://arsip.siap-ppdb.com/{year}/api/cari?no_daftar={deeper[4]}', headers=headers).json()
                        # print(url2)
                        # break
                        #nilai UN
                        #print(url2)
                        s.siswa_id = url2[0][-1][0][-1]
                        #print(s.siswa_id)
                        
                        nilaiBase = url2[2][-1]
                        nilai_list = []
                        for nilai in nilaiBase:
                            nilai_list.append(nilai[-1][0])
                        s.nilai = js.dumps(nilai_list)
                        
                        # acc
                        s.acc = url2[-1][-1][1][-2]
                        
                        # pilihan & jurusan
                        pilihanBase = url2[-2][-1]
                        pilihanJurusan = []
                        for i in range(3):
                            try:
                                usedBase = pilihanBase[i][-1]
                                setattr(s, f'pilihan{i+1}', usedBase[0][-1])
                                pilihanJurusan.append(None)
                            except IndexError:
                                setattr(s, f'pilihan{i+1}', None)
                                pilihanJurusan.append(None)
                        s.pilihanPenjurusan= js.dumps(pilihanJurusan)
                        try:
                            s.save()
                        except IntegrityError:
                            print("INTEGRITY ERROR")
                    except ConnectionError:
                        print("CONNECTION ERROR")
                    else:
                        break
                # break Development


    return HttpResponse("HEELLL")

def input_summary(request):
    sekolahAll = [d for d in Sekolah.objects.all() ]
    # nilai all
    years = [str(j) for j in range(2017,2022)]
    i = 0
    arg = {}
    for year in years:
        tmp = {}
        for sekolah in sekolahAll:
            siswa_all = [s.nilai_total for s in Siswa.objects.filter(acc=sekolah.sekolah_id, year=year)]
            siswa_zonasi = [s.nilai_total for s in Siswa.objects.filter(acc=sekolah.sekolah_id, jalur='Jalur Zonasi', year=year)]

            siswa_all = list(map(float, siswa_all))
            siswa_zonasi = list(map(float, siswa_zonasi))

            max_siswa_all = max(siswa_all)
            min_siswa_all = min(siswa_all)
            avg_siswa_all = round(sum(siswa_all)/len(siswa_all), 2)

            max_siswa_zonasi = max(siswa_zonasi)
            min_siswa_zonasi = min(siswa_zonasi)
            avg_siswa_zonasi = round(sum(siswa_zonasi)/len(siswa_zonasi), 2)
            
            print(avg_siswa_zonasi, year)
            
            ringkasan_z = Ringkasan()
            ringkasan_a = Ringkasan()

            ringkasan_z.sekolah = sekolah
            ringkasan_a.sekolah = sekolah

            ringkasan_z.year = year
            ringkasan_a.year = year
            
            ringkasan_z.sum_type = 'zonasi'
            ringkasan_a.sum_type = 'all'
            
            ringkasan_z.high= max_siswa_zonasi
            ringkasan_a.high = max_siswa_all
            
            ringkasan_z.low = min_siswa_zonasi
            ringkasan_a.low = min_siswa_all

            ringkasan_z.rata2 = avg_siswa_zonasi
            ringkasan_a.rata2 = avg_siswa_all

            ringkasan_z.save()
            ringkasan_a.save()
            
            
            i += 1

    return JsonResponse(arg)

def input_prediction(request):
    with open('api/prediksi.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        for read in reader:
            if (len(read) != 0):
                sekolah = Sekolah.objects.get(pk=read[0])
                prediksi = Prediksi(sekolah=sekolah, prediksi=float(read[1]))
                prediksi.save()          

    return JsonResponse({
        'error': False
    })

# Main Endpoint

def ringkasan(requests):
    passed = {}
    
    tahun = [str(i) for i in range(2017, 2022)]

    if ('id' in requests.GET):
        try:
            sekolah = Sekolah.objects.get(pk=requests.GET['id'])
            tmp  = {}
            for year in tahun:
                ringkasan = Ringkasan.objects.filter(sekolah=sekolah, year=year)
                tmpAll, tmpZonasi = {}, {}
                # all
                for all in ringkasan.filter(sum_type='all'):
                    tmpAll['high'] = all.high
                    tmpAll['low'] = all.low
                    tmpAll['avg'] = all.rata2
                
                for zon in ringkasan.filter(sum_type='zonasi'):
                    tmpZonasi['high'] = all.high
                    tmpZonasi['low'] = all.low
                    tmpZonasi['avg'] = all.rata2

                tmp[year] = {
                    'all': tmpAll,
                    'zonasi': tmpZonasi,
                }
            passed['error'] = False
            passed['id'] = requests.GET['id']
            passed['data'] = tmp
        except:
            passed['error'] = True
            passed['id'] = requests.GET['id']
            passed['data'] = {}


    else:
        sekolah = Sekolah.objects.all()
        for s in sekolah:
            tmp = {}
            for year in tahun:
                data_zonasi = Ringkasan.objects.filter(sum_type='zonasi', sekolah=s, year=year)
                data_all = Ringkasan.objects.filter(sum_type='all', sekolah=s, year=year)
                tmpZonasi = {}
                tmpAll = {}
                
                for data in data_zonasi:
                    tmpZonasi['min'] = data.low
                    tmpZonasi['max'] = data.high
                    tmpZonasi['avg'] = data.rata2
                for data in data_all:
                    tmpAll['min'] = data.low
                    tmpAll['max'] = data.high
                    tmpAll['avg'] = data.rata2
                tmp[year] = {
                    'zonasi':tmpZonasi,
                    'all':tmpAll
                }
                
            passed[s.sekolah_id] = tmp
        
    
    return JsonResponse(passed)

def sekolahParser(request):
    sekolah_list_raw = Sekolah.objects.all()
    sekolah_list = []

    for sekolah in sekolah_list_raw:
        tmp = []
        tmp.append(sekolah.sekolah_id)
        tmp.append(sekolah.nama)
        tmp.append(sekolah.npsn)
        tmp.append(sekolah.kota)
        tmp.append(sekolah.logo)
        sekolah_list.append(tmp)

    return JsonResponse(sekolah_list, safe=False)
    
def prediksi(request):
    passed_data = {}

    if ('id' in request.GET):
        try:
            requested_id = request.GET['id']
            sekolah_target = Sekolah.objects.get(pk=requested_id)
            pred = Prediksi.objects.get(sekolah=sekolah_target)
            data = {}
            data['sekolah_id'] = sekolah_target.sekolah_id
            data['prediksi'] = pred.prediksi

            passed_data['error'] = False
            passed_data['data'] = data
        except Prediksi.DoesNotExist:
            passed_data['error'] = True
            passed_data['error_massage'] = 'Requested ID Not Found!'
            passed_data['data'] = {}
            
    else:
        passed_data['error'] = True
        passed_data['error_massage'] = 'parameter invalid'


    return JsonResponse(passed_data)

