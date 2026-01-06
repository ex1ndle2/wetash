
import requests


def fetch_air_quality(district):
    """Получить AQI с OpenWeatherMap API"""
    API_KEY= '3d10e4a298dc450e1b3e84319ab75b85'
    
    # Координаты районов Ташкента (примерные)
    coords = {
        'Yunusabad': (41.3333, 69.2887),
        'Chilanzar': (41.2742, 69.2036),
        'Mirzo Ulugbek': (41.3358, 69.3363),
        'Sergeli': (41.2264, 69.2235),
    }
    
    lat, lon = coords.get(district, (41.2995, 69.2401))
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        aqi = data['list'][0]['main']['aqi'] * 50  # Конвертируем в стандартный AQI
        return aqi
    except:
        return 75  # По умолчанию, если API не работает
    



