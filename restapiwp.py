import os
import requests
import base64


# Escribe en la api de Wordpress un articulo
class RestApiWP:

    def __init__(self, config, logging):
        self.logging = logging
        self.wp_site = config.get('WP', 'wp_site')
        self.wp_user = config.get('WP', 'wp_user')
        self.wp_password = os.environ["wp_password"]
        self.headers = None
        self.wp_api_posts_url = f'{self.wp_site}{config.get('WP', 'endpoint_posts_url')}'
        self.wp_categories_url = f'{self.wp_site}{config.get('WP', 'endpoint_categories_url')}'
        self.wp_tags_url = f'{self.wp_site}{config.get('WP', 'endpoint_tags_url')}'
        self.generateHeaders()

    # Genera la cabecera de la solicitud con las credenciales
    def generateHeaders(self):
        # Codificación Base64 de las credenciales
        credentials = f'{self.wp_user}:{self.wp_password}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        # Encabezados de la solicitud
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }

    # ----------------------------------------------------------------
    # Formato de entrada del Post
    #    new_post = {
    #    'title': 'Título2 del artículo',
    #    'content': 'Contenido del artículo',
    #    'status': 'draft',  # 'draft' para borradores, 'publish' para publicar
    #    'categories': ['Cat1', 'Cat2'], # o [] -> sin categorias
    #    'tags' : ['Tag1','Tag2'],        # o [] -> sin tags
    #    'excerpt': ''
    #    }
    # -----------------------------------------------------------------

    # Escribe un post
    def writePost(self, new_post):
        # Si indicamos categorias al articulo, detectamos si existen en WP.
        # En caso contrario se crean y se asocia al articulo
        if len(new_post['categories']) > 0:
            # Obtener o crear categorías
            category_ids = [self.get_or_create_category(cat)
                            for cat in new_post['categories']]
            new_post['categories'] = category_ids

        if len(new_post['tags']) > 0:
            # Obtener o crear tags
            tags_ids = [self.get_or_create_tag(tag)
                        for tag in new_post['tags']]
            new_post['tags'] = tags_ids
        try:
            response = requests.post(self.wp_api_posts_url,
                                     headers=self.headers,
                                     json=new_post)
        except Exception as err:
            self.logging.error(f"Error al escribir el post en WP {err}")
            raise

        return response

    # Función para obtener o crear una categoría
    def get_or_create_category(self, name):
        try:
            response = requests.get(self.wp_categories_url,
                                    headers=self.headers,
                                    params={'search': name})
            if response.status_code == 200 and response.json():
                return response.json()[0]['id']
            else:
                response = requests.post(self.wp_categories_url,
                                         headers=self.headers,
                                         json={'name': name})
                return response.json()['id']
        except Exception as err:
            self.logging.error(f"Error al recuperar o crear categorias en WP {err}")
            raise

    # Función para obtener o crear una etiqueta
    def get_or_create_tag(self, slug):
        try:
            response = requests.get(self.wp_tags_url,
                                    headers=self.headers, 
                                    params={'slug': slug})
            if response.status_code == 200 and response.json():
                return response.json()[0]['id']
            else:
                response = requests.post(self.wp_tags_url,
                                         headers=self.headers,
                                         json={'name': slug, 'slug': slug})
                return response.json()['id']
        except Exception as err:
            self.logging.error(f"Error al recuperar o crear tags en WP {err}")
            raise
