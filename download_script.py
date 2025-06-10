import requests
import os
import glob
import time
from datetime import datetime

def download_file(url, filename=None):
    """
    Скачивает файл по URL и сохраняет его
    """
    try:
        response = requests.get(url, stream=True)
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


def download_file2(url, filename=None, api_key=None):
    """
    Скачивает файл по URL с API ключом и сохраняет его
    """
    try:
        # Формируем заголовки
        if api_key:
            headers = {
                'accept': 'application/json',
                'apikey': api_key
            }
        else:
            headers = None
        
        # Делаем запрос с заголовками
        response = requests.get(url, headers=headers, stream=True)
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
    files = glob.glob("./downloads/file3_*.tmp")
    if not files:
        print("Файлов с маской file3_ не наёдено")
        return None
    
    # Получаем словарь {файл: время модификации} для всех файлов
    files_with_timestamp = {f: os.path.getmtime(f) for f in files}
    
    # Находим самый свежий файл
    latest_file = max(files_with_timestamp, key=files_with_timestamp.get)

    print(f"Найден самый свежий файл {latest_file}")
    return latest_file



if __name__ == "__main__":

    try:
        api_key = os.environ['API_KEY']
    except:
        api_key = None

    # URL файла для скачивания
    file_url = "https://weather.metoffice.gov.uk/forecast/u10j124jp#"  # Замените на нужный URL
    file_url2 = "https://api.open-meteo.com/v1/forecast?latitude=51.5053&longitude=0.055&hourly=temperature_2m&models=ukmo_uk_deterministic_2km&current=temperature_2m&temperature_unit=fahrenheit"
    file_url3 = "https://data.hub.api.metoffice.gov.uk/mo-site-specific-blended-probabilistic-forecast/1.0.0/collections/improver-probabilities-spot-uk/locations/00000005?parameter-name=probability_of_air_temperature_above_threshold%2Cprobability_of_air_temperature_above_threshold_maximum_PT12H%2Cprobability_of_air_temperature_above_threshold_minimum_PT12H" 

    # Добавляем timestamp к имени файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"file_{timestamp}.tmp"
    download_file2(file_url, filename)

    filename2 = f"file2_{timestamp}.tmp"
    download_file2(file_url2, filename2)

    filename3 = f"file3_{timestamp}.tmp"
    latest_file = get_latest_file3()
    if latest_file:
        last_modified = os.path.getmtime(latest_file)
        time_passed = time.time() - last_modified

        minutes_passed = time_passed / 60
        print(f"Прошло {minutes_passed:.1f} минут с последнего обновления")
        
        # Если прошло больше X минут - обновляем
        if time_passed > 25 * 60:
            #print("Существует недавний file3_")
            download_file2(file_url3, filename3, api_key)
        else:
            print("Прошло меньше X минут после обновления файла")
    else:
        # Если файлов вообще нет - скачиваем
        print("Файла file3_ вообще нет - скачиваем")
        download_file2(file_url3, filename3, api_key)