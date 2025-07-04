CÓMO USAR ESTE BACKEND:

1. Crear entorno virtual (opcional):
   python -m venv venv
   venv\Scripts\activate  (Windows) o source venv/bin/activate (Linux/Mac)

2. Instalar dependencias:
   pip install -r requirements.txt

3. Ejecutar servidor:
   uvicorn main:app --reload

4. Probar desde frontend o Postman con:
   POST http://localhost:8000/limpiar-audio
   Form-data con archivo de audio (.wav, .mp3, etc.)

Nota:
- Este backend simula limpieza de audio copiando el archivo.
- Para usar RNNoise real, debes instalar el binario y reemplazar shutil.copy(...) por subprocess.run(...)