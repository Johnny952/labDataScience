from typing import Dict, List, Optional
from fastapi import FastAPI
from joblib import load
from tinydb import TinyDB, Query
from datetime import datetime
from tinydb.operations import set


app = FastAPI(title="Lab 6")
Mediciones = Query()
# aquí carguen el modelo guardado (con load de joblib) y
model = load("modelo.joblib")
# el cliente de base de datos (con tinydb). Usen './db.json' como bbdd.
db = TinyDB("./db.json")

# Nota: En el caso que al guardar en la bbdd les salga una excepción del estilo JSONSerializable
# conviertan el tipo de dato a uno más sencillo.
# Por   , si al guardar la predicción les levanta este error, usen int(prediccion[0])
# para convertirla a un entero nativo de python.

# Nota 2: Las funciones ya están implementadas con todos sus parámetros. No deberían
# agregar más que esos.


@app.post("/potabilidad/")
async def predict_and_save(observation: Dict[str, float]):
    # implementar 1. aquí
    prediccion = model.predict([list(observation.values())])
    hoy=datetime.now()
    observation["Day"] = hoy.day
    observation["Month"] = hoy.month
    observation["Year"] = hoy.year
    observation["Prediction" ] =int(prediccion[0])
    id=db.insert(observation)
    return {"Potabilidad": int(prediccion[0]),'id':id}


@app.get("/potabilidad/")
async def read_all():
    # implementar 2 aquí.
    return db.all()


@app.get("/potabilidad_diaria/")
async def read_by_day(day: int, month: int, year: int):
    # implementar 3 aquí
    return db.search((Mediciones.Day == day) & (Mediciones.Month == month)& (Mediciones.Year == year))


@app.put("/potabilidad/")
async def update_by_day(day: int, month: int, year: int, new_prediction: int):
    # implementar 4 aquí
    return {'succes':True,'updated_items':db.update(set("Prediction", new_prediction),((Mediciones.Day == day) & (Mediciones.Month == month)& (Mediciones.Year == year)))}


@app.delete("/potabilidad/")
async def delete_by_day(day: int, month: int, year: int):
    # implementar 5 aquí
    return {'succes':True,'deleted_items':db.remove((Mediciones.Day == day) & (Mediciones.Month == month)& (Mediciones.Year == year))}
