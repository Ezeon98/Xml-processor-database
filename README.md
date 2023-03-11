# alembic migrations

## Create venv
```bash
python -m venv venv
```
## Activate venv

```bash
.\venv\Scripts\activate
```
## Install requirements into venv
```bash
pip install -r .\requirements.txt
```

## Alembic init
alembic init [schemaname]
Ej.
```bash
alembic init public 
```

## Create Revision
alembic revision -m "[message]"
Ej.
```bash
alembic revision -m "initial"
```

## Alembic uprades sql script
```bash
alembic upgrade head --sql
```

## Alembic uprades run into database
```bash
alembic upgrade head
```

## Agregar Modelos

1. Crear carpeta para modelos, puede ser cualquier nombre dentro de la cerpta correspondiente a la base
```bash
mkdir models
```
2. Crear init para módulo
```bash
\models> touch __init__.py
```
3. crear archivo para configurar la conexión a la base de datos
```bash
\models> touch database.py
```
```py
"""Configure database connection."""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```
4. Crear archivo que contenga los modelos
```bash
\models> touch models.py
```
```py
"""Configure database connection."""
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint, VARCHAR
from models.database import Base

class Arba(Base):
    """Arba"""

    __tablename__ = "arba_padron_general"
    __table_args__ = ({"postgresql_partition_by": "LIST (periodo)"},)
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    periodo = Column(String, primary_key=True)
    nro_grupo_percepcion = Column(String)
    fecha_publicacion = Column(DateTime)
    fecha_desde = Column(DateTime)
    fecha_hasta = Column(DateTime)
    cuit = Column(String)
    tipo_contr_insc = Column(String)
    marca_alta_sujeto = Column(String)
    marca_cambio_alicuota = Column(String)
    alicuota_percepcion = Column(Float)
    alicuota_retencion = Column(Float)
```
5. Crear init para módulo dentro de la carpeta de la base de datos. En este caso dbtest
```bash
\dbtest> touch __init__.py  
```
6. Modificar el archivo public\env.py

<img src="_readme_images\database-public-env.py.png" />

```py
from models.models import Arba
from models import database
```

```py
target_metadata = database.Base.metadata
```

```py
PG_HOST="host.docker.internal"
PG_PORT=5432
PG_DB="datareaderxmlchile"
PG_USER="datareaderxmlchile"
PG_PASSWORD="datareaderxmlchile"
SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{int(PG_PORT)}/{PG_DB}"
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
```

## Create Revision autogenerada en base a los modelos
alembic revision -m "[message]" --autogenerate
Ej.
```bash
alembic revision -m "initial" --autogenerate
```
