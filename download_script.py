import os
import requests
import glob
import json
import time
from datetime import datetime, timedelta, timezone



def download_file2(url, filename=None, api_key=None, headers_accept='application/json'):
    """
    Скачивает файл по URL с API ключом и сохраняет его
    """
    try:
        # Формируем заголовки
        if api_key:
            headers = {
                'accept': headers_accept,
                'apikey': api_key
            }
        else:
            headers = None
        
        # Делаем запрос с заголовками
        response = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        # Если имя файла не указано, извлекаем из URL
        if not filename:
            filename = url.split('/')[-1] or 'downloaded_file'
        
        # Создаем папку downloads если её нет
        os.makedirs('downloads', exist_ok=True)
        
        filepath = os.path.join('downloads', filename)
        
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Файл успешно скачан: {filepath}")
        print(f"Размер: {os.path.getsize(filepath)} байт")
        return filepath
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании: {e}")
        return None



def get_latest_file3():
    # Ищем все файлы с маской file3_*
    files = glob.glob("./downloads/met-proba/file3_*.tmp")
    if not files:
        print("Файлов с маской file3_ не найдено")
        return None
    
    # Просто находим максимальное имя файла. 
    # Так как формат даты YYYYMMDD_HHMMSS, сортировка строк сработает правильно.
    latest_file = max(files)

    print(f"Найден самый свежий файл (по имени): {latest_file}")
    return latest_file



if __name__ == "__main__":

    try:
        api_key3 = os.environ['API_KEY_MET_UK']
    except:
        api_key3 = None

    try:
        api_key4 = os.environ['API_KEY_MET_GLOB']
    except:
        api_key4 = None

    try:
        api_key_atmo = os.environ['API_KEY_MET_ATMO']
    except:
        api_key_atmo = None


    # URL файла для скачивания
    file_url = "https://weather.metoffice.gov.uk/forecast/u10j124jp#"  

    file_url2 = "https://api.open-meteo.com/v1/forecast?latitude=51.5053&longitude=0.055&hourly=temperature_2m&models=ukmo_uk_deterministic_2km&current=temperature_2m&temperature_unit=fahrenheit"

    file_url21 = "https://ensemble-api.open-meteo.com/v1/ensemble?latitude=51.5053&longitude=0.0553&hourly=temperature_2m&models=ukmo_uk_ensemble_2km&temperature_unit=fahrenheit"

    file_url3 = "https://data.hub.api.metoffice.gov.uk/mo-site-specific-blended-probabilistic-forecast/1.0.0/collections/improver-probabilities-spot-uk/locations/00000005?parameter-name=probability_of_air_temperature_above_threshold%2Cprobability_of_air_temperature_above_threshold_maximum_PT12H%2Cprobability_of_air_temperature_above_threshold_minimum_PT12H" 

    file_url4 = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly?latitude=51.5053&longitude=0.0553"


    # Добавляем timestamp к имени файла
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"site/file_{timestamp}.tmp"
    download_file2(file_url, filename)

    filename2 = f"open-deterministic/file2_{timestamp}.tmp"
    download_file2(file_url2, filename2)

    filename21 = f"open-ensemble/file21_{timestamp}.tmp"
    download_file2(file_url21, filename21)

    filename3 = f"met-proba/file3_{timestamp}.tmp"
    filename4 = f"met-site-specific/file4_{timestamp}.tmp"

    latest_file = get_latest_file3()
    if latest_file:
        #last_modified = os.path.getmtime(latest_file)
        #time_passed = time.time() - last_modified

        timestamp_str = os.path.basename(latest_file)[6:-4] # Убираем 'file3_' и '.tmp'
        # Превращаем строку в объект datetime
        file_datetime = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)

        time_passed_delta = datetime.now(timezone.utc) - file_datetime
        minutes_passed = time_passed_delta.total_seconds() / 60

        print(f"Время файла по его имени: {file_datetime}")
        print(f"Прошло {minutes_passed:.1f} минут с последнего обновления")
        
        # Если прошло больше X минут - обновляем
        #if time_passed > 25 * 60:
        if time_passed_delta > timedelta(minutes=25):
            #print("Существует недавний file3_")
            #download_file2(file_url3, filename3, api_key3)
            download_file2(file_url4, filename4, api_key4)
        else:
            print("Прошло меньше X минут после обновления файла")
    else:
        # Если файлов вообще нет - скачиваем
        print("Файла file3_ вообще нет - скачиваем")
        #download_file2(file_url3, filename3, api_key3)
        download_file2(file_url4, filename4, api_key4)



    file_url_atmolatest = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0/orders/o220948200789/latest?detail=MINIMAL&dataSpec=1.0.0"
    filename_atmolatest = 'atmosph/file_atmo_latest.json'

    download_file2(file_url_atmolatest, filename_atmolatest, api_key_atmo)

    with open('./downloads/atmosph/file_atmo_latest.json') as f:
        dict_ = json.load(f)

    available_fileid = list()
    for i in range(len(dict_['orderDetails']['files'])):
        fileid = dict_['orderDetails']['files'][i]['fileId']
        if len(fileid.split('_')[-1])>4:
            available_fileid.append(fileid)


    files = os.listdir("./downloads/atmosph/")
    for fileid in sorted(available_fileid)[-3:]:
        fname = fileid + '.dat'
        if fname not in files:
            print(f"{fname} downloading")
            filename_atmodata = f"atmosph/{fileid}.dat"
            file_url_atmodata = f"https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0/orders/o220948200789/latest/{fileid}/data"
            file_url_atmodata = file_url_atmodata.replace('+','%2B')
            headers_accept = 'application/x-grib'

            download_file2(file_url_atmodata, filename_atmodata, api_key_atmo, headers_accept)
        else:
            print(f"{fname} already downloaded")
