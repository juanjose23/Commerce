# Projects 2 commerce

Este proyecto es un sitio de subastas que permite a los usuarios crear, ver y gestionar listados de subastas, realizar ofertas, añadir comentarios, y administrar una lista de seguimiento. A continuación se detallan las características y el uso del sitio.

## Modelos

La aplicación incluye al menos los siguientes modelos además del modelo `User`:
1. **Category**: Representa un listado de categoria.
2. **Listing**: Representa un listado de subasta.
3. **Bid**: Representa una oferta realizada en un listado.
4. **Comment**: Representa un comentario realizado en un listado.
5. **Watchlist** (Opcional): Representa la lista de seguimiento de un usuario.


## Funcionalidades

### 1. Crear Listado

- **Descripción**: Los usuarios pueden crear un nuevo listado de subasta.
- **Características**:
  - El usuario puede especificar un título, una descripción y una oferta inicial.
  - Opcionalmente, puede proporcionar una URL para una imagen y/o una categoría.

### 2. Página de Listados Activos

- **Descripción**: Muestra todos los listados de subastas actualmente activos.
- **Características**:
  - Se muestra el título, descripción, precio actual y foto (si existe) para cada listado.

### 3. Página de Listado

- **Descripción**: Muestra los detalles completos de un listado de subasta.
- **Características**:
  - Los usuarios pueden ver el precio actual y añadir el artículo a su lista de seguimiento (si están autenticados).
  - Los usuarios autenticados pueden realizar ofertas (deben ser mayores que la oferta inicial y cualquier otra oferta existente).
  - Los creadores del listado pueden cerrar la subasta.
  - Los usuarios ganadores de la subasta recibirán una notificación en la página de listado cerrado.
  - Los usuarios autenticados pueden añadir comentarios y ver todos los comentarios realizados en el listado.

### 4. Lista de Seguimiento

- **Descripción**: Muestra todos los listados añadidos a la lista de seguimiento del usuario.
- **Características**:
  - Los usuarios autenticados pueden ver y acceder a los listados de su lista de seguimiento.

### 5. Categorías

- **Descripción**: Muestra todas las categorías disponibles y los listados activos en cada categoría.
- **Características**:
  - Al hacer clic en una categoría, el usuario puede ver todos los listados activos en esa categoría.

### 6. Interfaz de Administración de Django

- **Descripción**: Permite a un administrador del sitio ver, añadir, editar y eliminar listados, comentarios y ofertas.
- **Características**:
  - Los administradores pueden gestionar todos los aspectos del sitio a través de la interfaz de administración de Django.

## Instalación

1. **Clonar el Repositorio**

    ```bash
    git clone https://github.com/juanjose23/cocomer.git
    cd sitio-subastas
    ```

2. **Instalar Dependencias**

    - Asegúrate de tener Python y Django instalados.
    - Instala las dependencias necesarias usando pip.

    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar la Base de Datos**

    - Realiza las migraciones necesarias para crear las tablas en la base de datos.

    ```bash
    python manage.py migrate
    ```

4. **Ejecutar el Servidor**

    - Inicia el servidor de desarrollo.

    ```bash
    python manage.py runserver
    ```

## Uso

1. **Crear Listado**: Accede a la página de creación de listados para añadir un nuevo listado de subasta.

2. **Ver Listados Activos**: La página principal muestra todos los listados activos.

3. **Página de Listado**: Haz clic en un listado para ver sus detalles y realizar ofertas.

4. **Lista de Seguimiento**: Visita la página de lista de seguimiento para gestionar tus listados favoritos.

5. **Categorías**: Navega por las categorías para explorar listados en cada categoría.

6. **Interfaz de Administración**: Los administradores pueden acceder a la interfaz de administración para gestionar el sitio.

## Contribuciones

Si encuentras algún error o deseas realizar mejoras, siéntete libre de bifurcar el repositorio y enviar solicitudes de extracción.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
