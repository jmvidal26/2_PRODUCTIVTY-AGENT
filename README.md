## Productivity Agent_ES

Asistente de productividad inteligente diseñado para gestionar flujos de trabajo mediante un sistema de "Cerebro Dual" (Local + Nube).

## Características Principales
- *Inteligencia Híbrida:* Alterna automáticamente entre **Gemini 1.5 Flash** (vía `google-genai`) cuando hay conexión y **Gemma 2:2b** (vía Ollama) en modo offline.
- *Multiprocesamiento Async:* Interfaz construida en **Pygame** que se comunica de forma asíncrona con procesos de lógica en Python y optimización en **C++**.
- *Análisis NLP:* Implementación de **SpaCy** para lematización y análisis de patrones de usuario.
- *Seguridad:* Gestión de credenciales mediante variables de entorno (`python-dotenv`).

## Instalación y Uso

- Clone el repositorio con: git clone [https://github.com/jmvidal26/2_PRODUCTIVTY-AGENT](https://github.com/jmvidal26/2_PRODUCTIVTY-AGENT)

- Instale los requerimientos con: pip install -r requirements.txt

- Cree un archivo .env y añada su llave: GEMINI_API_KEY=tu_llave_aqui

- Ejecute con: python core/testing_ui_async.py
