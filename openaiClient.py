import os
from openai import OpenAI

"""
Clase que se encarga de generar el articulo:
- Primero se le solicita que genere un esquema del articulo sobre 
  la keyword pasada
- Genera un título
- Genera el articulo, contenido, basado en el esquema generado anteriormente
- Genera la meta description
"""


class OpenaiClient: 
    def __init__(self, config, logging) -> None:
        self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.model = config.get('APP', 'model')
        self.logging = logging
    
    # Genera un esquema relacionado con la keyword
    def generateOutline(self, keywords):
        print('Generando esquema .....')
        role = "Eres un experto en escritura de blogs basados en Wordpress"
        prompt = f"Crea un esquema detallado sobre: {keywords}. Los encabezados deben indicar las etiquetas <h2>, <h3> y <h4> adecuadas respectivamente. El esquema debe cubrir el tema en profundidad. El esquema ha de realizarse en Español"
        try:
            response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": role},
                            {"role": "user", "content": prompt}
                        ],
                        n=1,
                        stop=None,
                        temperature=0.7,
                        )
        except Exception as err:
            self.logging.error(f"Error al generar el esquema {err}")
            raise
        return response.choices[0].message.content.strip()
    
    # Genera el titulo del articulo
    def generateTitle(self, keywords):
        print("Generando título .....")
        role = "Eres un experto en escritura de blogs basados en Wordpress"
        prompt = f"Cree un título breve, relevante y conciso para {keywords} que coincida con la intención de búsqueda respectiva. NO pongas el título entre comillas. Se creativo"
        try:
            response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": role},
                            {"role": "user", "content": prompt}
                        ],
                        n=1,
                        stop=None,
                        temperature=0.7,
                        )
        except Exception as err:
            self.logging.error(f"Error al generar el titulo {err}")
            raise
        return response.choices[0].message.content.strip()
    
    # Genera el articulo (Contenido) basado en el esquema
    def generateContent(self, keywords, outline):
        print("Generando contenido .....")
        role = "Eres un experto en escritura de articulos en blogs basados en Wordpress"
        additional_prompt = "Por favor, escribe un articulo SEO frienly, creativo y desde el punto de vista técnico con el objetivo de educar al lector con el articulo. Por favor, asegurese que los encabezados principales del articulo esten formateadas usando <h2> y los subtitulos con <h3>. "
        prompt = f"Quiero que elabores un artículo detallado y amplio sobre {keywords} utilizando el esquema {outline}. Asegurate de usar 4 veces las {keywords} a traves  del articulo manteniendo una densidad de palabras claves (keyword density) del 3 %. {additional_prompt}"
        try:
            response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": role},
                            {"role": "user", "content": prompt}
                        ],
                        n=1,
                        stop=None,
                        temperature=0.7,
                        )
        except Exception as err:
            self.logging.error(f"Error al generar el contenido {err}")
            raise
        return response.choices[0].message.content.strip()
    
    # Genera la meta description del articulo
    def generate_meta_description(self, content):
        print("Generando meta description .....")
        role = "Eres un experto en escritura de articulos en blogs basados en Wordpress"
        prompt = f"Escribe una meta descripción atractiva para {content}. No más de 160 caracteres."
        try:
            response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": role},
                            {"role": "user", "content": prompt}
                        ],
                        n=1,
                        stop=None,
                        temperature=0.7,
                        )
        except Exception as err:
            self.logging.error(f"Error al generar la meta description {err}")
            raise
        return response.choices[0].message.content.strip()