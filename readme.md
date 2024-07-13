# Generador de artículos para Wordpress, generados por IA (ChatGPT)

## Introducción

Se pretende realizar una app que automatice y genere artículos *SEO Friendly* para un blog Wordpress mediante IA, usando Chatgpt. Una vez generado dicho artículo se escribirá en el Wordpress a través de su RESTAPI.
El proceso será el siguiente:

 - Introduciremos en un fichero de texto llamado **kewords.txt** sobre que queremos que chatgpt nos genere el articulo. Es recomendable, ser un poco creativo con la keyword, por ejemplo, si estamos escribiendo en un blog sobre nootrópicos y queremos que nos genere una entrada sobre la L-Tirosina, deberíamos poner algo asi como: ***L-Tirosina como nootropico*** en vez de poner solo "L-Tirosina". Cada Keyword, debe de ocupar una linea en el fichero.
 - Ejecutaremos el script y éste nos generará:
		 - Un título del artículo basado en la keyword.
		 - Un esquema sobre la keyword con sus secciones y títulos correspondientes.
		 - Genera el artículo basado en el esquema anterior, estructurado con sus títulos y subtítulos y Seo Friendly usando la keyword dentro del articulo.
		 - Genera una *Meta Description* atractiva de no mas de 160 caracteres.
 - Una vez generado el articulo, se escribe en el Wordpress a través de su RESTAPI.
 - Si no ha habido errores se escribe la keyword usada en un fichero llamado: **usedkeywords.txt** y se elimina de **keywords.txt** .
 - Y pasaría a la siguiente keyword del fichero kywords.txt, así hasta que se haya finalizado todas.

## Consideraciones:

 - Es una automatización que nos permitiría generar decenas o cientos de artículos.
 - Dependiendo del modelo que usamos de Openai (GPT-4o, GPT 4Turbo, GPT-3.5Turbo, etc) puede tardar más o menos en generar el artículo, al final de este documento presentaremos algunas soluciones para evitar bloqueos o procesos largos. Otro tanto ocurre con el coste del servicio, modelos antiguos como GPT-3.5Turbo son mas económicos que GPT-4o, pero este último genera artículos mas elaborados y de mejor calidad. Independientemente de  todo esto es económico y sobre todo el ahorro de tiempo que tendremos al generar los artículos.
 - Tienes que tener crédito, para ello puedes recargar a través de https://platform.openai.com/
 - Es conveniente siempre revisar los artículos, por defecto los artículos generados se escriben en el Wordpress en modo *Draft o Borrador* ( aunque podemos cambiarlo en el código para que lo escriba en modo *Publish* pero no lo recomiendo).
 - En el repositorio he añadido una instancia de Wordpress/Mysql para Docker Compose para que puedas hacer pruebas en local, solo tienes que tener instalado Docker Desktop en tu maquina https://www.docker.com/products/docker-desktop/ . Más adelante te indico las instrucciones para levantar las instancias.

## Librerías usadas:

 - **configparser** https://docs.python.org/3/library/configparser.html Lib para leer ficheros de configuración.
 - **openai** Acceso al RestApi de OpenAI
 - **requests** Librería para realización de peticiones http.
 - **python-docx** Librería para la generación de ficheros.docx
 - **python-dotenv** Librería para lectura de ficheros .env

## Configuración e instalación.

 1. Clona el proyecto donde quieras en tu equipo local.
 2. Dentro del proyecto dispones de un fichero *docker-compose.yml* que te permite si no dispones de un Wordpress en un hosting, levantar una instancia de Wordpress y Mysql en local usando Docker, para la realización de pruebas. Para ello tienes que tener instalado en tu equipo Docker Desktop. Para descargar las imágenes y levantar ejecuta el siguiente comando dentro de la carpeta del proyecto:  `docker-compose up -d` Por defecto se levantaría en la dirección http://localhost:8000  (Puedes editar el fichero YAML y cambiar el puerto, asi como los usuarios y contraseñas del Wordpress y el de MySQL).
 3. Crea un fichero .ENV en el directorio del proyecto, dentro has de añadir dos lineas:

    wp_password="password del usuario con rol de Editor" 
    OPENAI_API_KEY="Tu clave de openai"
    
	**wp_password** representa la contraseña de un usuario que crearemos 		dentro de WP con rol de Editor. Y **OPENAI_API_KEY** la clave que necesitas de openai y que puedes generarla en https://platform.openai.com/

 4. En el fichero *settings.ini* dispones de las siguientes lineas:

     [WP]
    wp_site = http://localhost:8000
    wp_user = script
    endpoint_posts_url = /wp-json/wp/v2/posts
    endpoint_categories_url = /wp-json/wp/v2/categories
    endpoint_tags_url = /wp-json/wp/v2/tags
    [APP]
    model = gpt-4o
    
	En la sección WP dispones de la url donde se encuentre nuestra instancia de Wordpress (corresponde con la url del fichero docker compose), asi como el nombre del usuario que creamos con el rol de Editor, su contraseña ya vimos que está contenida en el *.env* y a continuación se encuentran los endpoints de la Rest Api de Wordpress para poder escribir posts, categorías y tags.
En la sección APP puedes añadir el modelo que desees de OpenAI, dispones de varios modelos, elegimos el *gpt-40* por ser el último y el mas creativo de todos, pero el más caro. 

 5. En tu instancia de Wordpress hay que añadir algo de seguridad a la RestApi, para ello instala el siguiente plugin: https://wordpress.org/plugins/wp-rest-api-authentication/ una vez instalado y activado selecciona : **Basic authentication** y mas adelante: **username & password with Base64 encoding**
 6. Crea un entorno virtual, por ejemplo: `python3 -m venv venv`
 7. Instala todas las dependencias:  `pip install -r requeriments.txt`
 8. Añade la keyword o keywords en el fichero *keywords.txt*, una por linea.
 9. Ejecuta el script, mediante: `python3 main.py` Si no hay errores, el script ira generando mensajes por pantalla de las acciones que va realizando hasta escribir el post en la REST-Api y por ultimo guarda el articulo generado en un fichero con formato .DOCX en la carpeta DOCX. En el supuesto de que hubiera algún error o alguna excepción, el script genera un fichero **error.log** con información detallada para poder depurar y así poder solucionarlo.

## Estructura de un post

    #Formato de entrada del Post
        new_post = {
	        'title': 'Título2 del artículo',
	        'content': 'Contenido del artículo',
	        'status': 'draft',  # 'draft' para borradores, 'publish' para publicar
	        'categories': ['Cat1', 'Cat2'], # o [] -> sin categorias
	        'tags' : ['Tag1','Tag2'],        # o [] -> sin tags
	        'excerpt': ''
        }
   Esta será la estructura del post con el cual generaremos el articulo para escribirlo en la RestAPi de WP, pasemos a describirlo un poco.
   

 - *title* -> Es el titulo del post/artículo, generado por chatgpt.
 - *content* -> es el artículo en si generado por chatgpt y basado en la estructura del esquema que previamente se ha generado.
 - *status* -> Borrador o Publicado, por defecto se publica el artículo en modo borrador. Chatgpt recomienda no fiarse del contenido generado y por ende recomendamos que antes de publicarlo se revise, por esa opción por defecto lo creamos en modo borrador.
 - *categories* -> Podemos añadir las categorías del articulo, el script las busca antes y si no están en Wordpress las crean y las asigna al articulo. Si no queremos asignarle categorías y se la asignamos manualmente en Wordpress se pone los corchetes vacíos.
 - *tags* -> Podemos asignar tags al articulo, en caso de no estar en Wordpress previamente las crea y luego se las asigna al articulo. Si no queremos asignar tags al artículo le ponemos los corchetes vacíos.
 - *excerpt* -> es la meta descripcion generado por chatGPT de no mas de 160 caracteres.

## Mejoras y recomendaciones

 - Puedes cambiar y jugar con los prompts de chatgpt para la generación de contenidos.
 - Prueba con distintos modelos de openai: https://platform.openai.com/docs/models. Solo tienes que añadir el modelo en el fichero settings.ini
 - Depende del modelo, puede tardar en generar el contenido, por lo que si al final si quieres usar este script de modo masivo deberías de implementar algún sistema de colas para mejorar el rendimiento, por ejemplo *Celery (Redis o RabbitMQ)*
 - Por defecto no genera imágenes en el artículo y tendrías que asignársela a mano en Wordpress, podrías modificar si quieres el script y que mediante el modelo *DALL·E* te generará la imagen y añadirla a la entrada.
 - Normalmente en SEO se suelen crear varios blog satélites, como este script te guarda el artículo generado en formato DOCX en local, puedes reaprovechar dicho artículo "reescribiendolo" usando otro modelo, por ejemplo el *Claude 3.5 sonnet* y de esa forma usarlos en otros blogs.

Eres libre de usar este script para tu uso y para el fin que quieras.

## Versiones:

 - Version 0.9 : Julio 2024. Commit inicial.
