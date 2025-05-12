from functools import lru_cache
import json
import requests
import time
from colorama import Fore, Style, init
import os
from dotenv import load_dotenv
from .cache_manager import CacheManager
from .config import CACHE_CONFIG
import logging

class FreshServiceAPI:
    def __init__(self):
        init(autoreset=True)
        load_dotenv()
        self.subdomain = os.getenv('FRESHSERVICE_SUBDOMAIN')
        self.api_key = os.getenv('FRESHSERVICE_API_KEY')
        self.base_url = f'https://{self.subdomain}.freshservice.com/api/v2/'
        self.request_counter = 0
        self.cache = CacheManager()
        self.logger = logging.getLogger(__name__)

    def handle_rate_limit(self, response):
        """Handle API rate limiting"""
        if response.status_code == 429:
            wait_time = int(response.headers.get('Retry-After', 60))
            print(f"{Fore.YELLOW}Rate limit reached. Waiting {wait_time} seconds...{Style.RESET_ALL}")
            time.sleep(wait_time)
            self.request_counter = 0
            return True
        return False

    def get_cached_request(self, endpoint):
        """Get cached request or make new one"""
        try:
            # Determinar el tipo de caché basado en el endpoint
            endpoint_parts = endpoint.split('/')
            cache_type = endpoint_parts[0] if endpoint_parts else 'general'
            
            logging.debug(f"Checking cache for endpoint: {endpoint} (type: {cache_type})")
            
            # Verificar si el endpoint está en la lista de excluidos
            if cache_type in CACHE_CONFIG.get('excluded_endpoints', []):
                logging.debug(f"Endpoint {endpoint} excluded from cache")
                return self.make_request(endpoint)
            
            # Intentar obtener de la caché
            cached_data = self.cache.get(endpoint, cache_type=cache_type)
            if cached_data is not None:
                logging.info(f"Cache hit for {endpoint}")
                return cached_data
            
            # Si no está en caché, hacer la petición
            logging.debug(f"Cache miss for {endpoint}, making request")
            data = self.make_request(endpoint, max_retries=3)  # Añadimos max_retries
            
            # Guardar en caché solo si la petición fue exitosa
            if data is not None:
                logging.debug(f"Caching response for {endpoint}")
                self.cache.set(endpoint, data, cache_type=cache_type)
                return data
            else:
                logging.warning(f"No se pudo obtener datos para {endpoint} después de reintentos")
                return None
            
        except Exception as e:
            logging.error(f"Error in cached request for {endpoint}: {e}")
            # Intentamos con reintentos en caso de error
            return self.make_request(endpoint, max_retries=3)

    def make_request(self, endpoint, method='GET', params=None, data=None, max_retries=3):
        """Make API request with simplified logging"""
        endpoint = endpoint.lstrip('/')
        url = f'{self.base_url}{endpoint}'
        
        logger = logging.getLogger(__name__)
        logger.info(f"API Request: {method} {url}")
        
        retries = 0
        while retries <= max_retries:
            try:
                response = requests.request(
                    method,
                    url,
                    auth=(self.api_key, ''),
                    params=params,
                    json=data,
                    timeout=30
                )
                
                logger.info(f"Response status: {response.status_code}")
                
                # Verificar rate limit
                if response.status_code == 429:
                    if self.handle_rate_limit(response):
                        retries += 1
                        logger.warning(f"Rate limit alcanzado. Reintento {retries}/{max_retries}")
                        continue
                
                if response.status_code != 200:
                    logger.error(f"Error response: {response.text}")
                    return None
                    
                return response.json()
                
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                retries += 1
                if retries <= max_retries:
                    logger.warning(f"Reintentando petición ({retries}/{max_retries})...")
                    time.sleep(5)  # Esperar antes de reintentar
                else:
                    return None
        
        return None

    def fetch_all_pages(self, endpoint, key):
        page = 1
        all_data = []
        max_retries = 3
        retry_count = 0
        
        while True:
            current_endpoint = f"{endpoint}?page={page}"
            data = self.make_request(current_endpoint, max_retries=max_retries)
            
            if not data:
                # Si no hay datos y aún tenemos reintentos, intentamos nuevamente
                retry_count += 1
                if retry_count <= max_retries:
                    logging.warning(f"Error al obtener página {page}, reintentando ({retry_count}/{max_retries})...")
                    time.sleep(5)  # Esperar antes de reintentar
                    continue
                else:
                    logging.error(f"No se pudo obtener datos para la página {page} después de {max_retries} intentos")
                    break
            
            # Resetear contador de reintentos si tuvimos éxito
            retry_count = 0
            
            if key not in data or not data[key]:
                break
                
            all_data.extend(data[key])
            page += 1
            logging.info(f"Obtenida página {page-1} con {len(data[key])} elementos")
            
        return all_data

    def fetch_paginated_data(self, endpoint, query=''):
        """Fetch all paginated data from an endpoint"""
        all_data = []
        page = 1
        max_retries = 3
        retry_count = 0
        
        while True:
            separator = '&' if '?' in query else '?'
            current_endpoint = f'{endpoint}{query}{separator}page={page}'
            
            # Usar max_retries para manejar rate limits
            data = self.make_request(current_endpoint, max_retries=max_retries)
            
            if not data:
                # Si no hay datos y aún tenemos reintentos, intentamos nuevamente
                retry_count += 1
                if retry_count <= max_retries:
                    logging.warning(f"Error al obtener página {page}, reintentando ({retry_count}/{max_retries})...")
                    time.sleep(5)  # Esperar antes de reintentar
                    continue
                else:
                    logging.error(f"No se pudo obtener datos para la página {page} después de {max_retries} intentos")
                    break
            
            # Resetear contador de reintentos si tuvimos éxito
            retry_count = 0
                
            # Extract data based on endpoint type
            key = endpoint.split('/')[0]  # assets, departments, locations, etc.
            if key in data and data[key]:
                all_data.extend(data[key])
                page += 1
                logging.info(f"Obtenida página {page-1} con {len(data[key])} elementos")
            else:
                logging.info(f"No hay más datos en la página {page}")
                break
                
        return all_data

    def get_cached_data(self, url):
        """Get cached data from API"""
        return self.get_cached_request(url)
