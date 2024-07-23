
#v10
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL base de la página
base_url = 'https://www.aepd.es/informes-y-resoluciones/informes-juridicos?page='

# Número de páginas
num_pages = 123  # Número total de páginas

# Lista para almacenar los datos
data = []

for page in range(0, num_pages + 1):
    url = f'{base_url}{page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar todos los enlaces que contienen .pdf en el atributo href
    pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$'))
    
    # Encontrar todas las fechas
    time_elements = soup.find_all('time', class_='datetime')
    
    for link in pdf_links:
        # Obtener el título del informe
        title_element = link.text.strip()
        if title_element:
            title = f"Informe jurídico {title_element}"  # Formato requerido del título
        else:
            title = 'Título no encontrado'
        
        # Construir el enlace completo
        full_link = 'https://www.aepd.es' + link['href']
        
        # Buscar la fecha asociada
        time_html = 'Fecha no disponible'
        for time_element in time_elements:
            time_html = time_element.get_text(strip=True)
            break  # Usamos la primera fecha encontrada, aunque esto puede ser refinado
        
        data.append({
            'Nombre': title,
            'Link': full_link,
            'Fecha': time_html
        })
    
    # Mensaje de progreso
    print(f'Se agregó página {page}')

# Crear un DataFrame de pandas y guardarlo como CSV
df = pd.DataFrame(data)
df.to_csv('informes_juridicos_links.csv', index=False, encoding='utf-8-sig')

print("Proceso completado y datos guardados en 'informes_juridicos_links.csv'")
