import requests
import os
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

if __name__ == "__main__":
    # URL файла для скачивания
    file_url = "https://weather.metoffice.gov.uk/forecast/u10j124jp#?date=2025-05-31"  # Замените на нужный URL
    
    # Добавляем timestamp к имени файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"file_{timestamp}.tmp"
    
    download_file(file_url, filename)