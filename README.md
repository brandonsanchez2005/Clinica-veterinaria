# Sistema de Gestión Veterinaria

API REST desarrollada con Django y Django REST Framework para administrar propietarios, mascotas y consultas veterinarias.

## Tecnologías

- Python
- Django
- Django REST Framework
- SQLite
- Autenticación por token

## Instalación

```powershell
git clone <URL_DEL_REPOSITORIO>
cd Clinica-veterinaria

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install django djangorestframework
```

## Configuración de base de datos

Aplicar las migraciones:

```powershell
python manage.py migrate
```

Crear un usuario administrador:

```powershell
python manage.py createsuperuser
```

## Ejecución

Iniciar el servidor:

```powershell
python manage.py runserver
```

La API estará disponible en:

```text
http://127.0.0.1:8000/clinica/
```

El panel administrativo estará disponible en:

```text
http://127.0.0.1:8000/admin/
```

## Pruebas automatizadas

Ejecutar las pruebas:

```powershell
python manage.py test
```

## Autenticación

Para obtener un token, enviar una solicitud `POST` a:

```text
/clinica/api/token/
```

Con el siguiente cuerpo JSON:

```json
{
  "username": "nombre_de_usuario",
  "password": "contraseña"
}
```

Para acceder a rutas protegidas, enviar el header:

```text
Authorization: Token tu_token_aqui
```

## Endpoints de la API
| Método | URL | Descripción | Parámetros / Body | Respuesta | Códigos |
|---|---|---|---|---|---|
| GET | `/clinica/` | Verifica que la API esté activa. | — | Mensaje de texto. | 200 |
| POST | `/clinica/api/token/` | Obtiene un token de autenticación. | `username`, `password`. | Token del usuario. | 200, 400 |
| GET | `/clinica/api/mascotas/` | Lista mascotas paginadas. | `page`, `especie`, `activas`, `propietario`. | Página, totales y resultados. | 200 |
| POST | `/clinica/api/mascotas/` | Registra una mascota. | JSON con nombre, especie, raza, fecha_nacimiento, peso, activo y propietario. | Mascota creada. | 201, 400 |
| GET | `/clinica/api/mascotas/<id>/` | Obtiene el detalle de una mascota. | ID en la URL. | Datos de la mascota. | 200, 404 |
| PUT / PATCH | `/clinica/api/mascotas/<id>/` | Actualiza una mascota. | ID y JSON con datos completos o parciales. | Mascota actualizada. | 200, 400, 404 |
| DELETE | `/clinica/api/mascotas/<id>/` | Elimina una mascota. | ID en la URL. | Sin contenido. | 204, 404 |
| GET | `/clinica/api/propietarios/` | Lista propietarios. | — | Lista de propietarios. | 200 |
| POST | `/clinica/api/propietarios/` | Registra un propietario. | JSON con identificación, nombre, teléfono y email opcional. | Propietario creado. | 201, 400 |
| GET | `/clinica/api/consultas/` | Lista consultas veterinarias. | — | Lista de consultas. | 200 |
| POST | `/clinica/api/consultas/` | Registra una consulta. | JSON con mascota, motivo, diagnóstico, tratamiento y costo. | Consulta creada. | 201, 400 |
| GET | `/clinica/api/perfil/` | Muestra el perfil del usuario autenticado. | Header `Authorization: Token <token>`. | ID, usuario y email. | 200, 401 |
| GET | `/clinica/api/estadisticas/` | Muestra estadísticas de la clínica. | Token de administrador. | Totales de propietarios, mascotas, activas y consultas. | 200, 401, 403 |
| GET | `/clinica/api/sesion/` | Incrementa y devuelve el contador de sesión. | — | Número de visitas de la sesión. | 200 |


## Reflexión final
Cuando Postman envía un POST para registrar una consulta veterinaria, la URL `/clinica/api/consultas/` dirige la solicitud a la View `api_consultas`. La View recibe los datos en `request.data` y crea una instancia de `ConsultaVeterinariaSerializer`. El Serializer realiza la validación de los campos, por ejemplo que el costo no sea negativo y que el motivo sea válido. Si los datos son correctos, el Serializer usa el Model `ConsultaVeterinaria` y el ORM de Django para guardar el registro en la base de datos. La relación con la mascota se establece mediante su identificador. Finalmente, la View devuelve una `Response` JSON con la consulta creada y el código HTTP 201. Si la validación falla, devuelve una Response con los errores y código 400.
