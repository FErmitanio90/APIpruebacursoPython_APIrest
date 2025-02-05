from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos la API
app = FastAPI()

# Definimos el modelo de datos
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simulamos una base de datos con una lista
cursos_db = []

# Obtener todos los cursos
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# Crear un nuevo curso
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # Generar un ID único
    cursos_db.append(curso)
    return curso  # Retornar el curso creado

# Obtener un curso por ID
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((c for c in cursos_db if c.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# Actualizar un curso por ID
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((c for c in cursos_db if c.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    curso_actualizado.id = curso_id  # Asegurar que el ID se mantenga igual
    index = cursos_db.index(curso)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# Eliminar un curso por ID
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next((c for c in cursos_db if c.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    cursos_db.remove(curso)
    return curso  # Retornar el curso eliminado

