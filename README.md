## Productivity Agent_ES (Legacy Version)

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



## Productivity Agent_En (Legacy Version)

Intelligent productivity assistant designed to manage workflows through a "Dual-Brain" system (Local + Cloud).

## Key Features

-*Hybrid Intelligence:* Automatically toggles between Gemini 1.5 Flash (via google-genai) for online processing and Gemma 2:2b (via Ollama) for offline mode.

-*Async Multiprocessing:* Custom Pygame interface communicating asynchronously with Python logic processes and C++ optimization modules.

-*NLP Analysis:* Powered by SpaCy for lemmatization and user behavioral pattern analysis.

-*Security:* Robust credential management using environment variables (python-dotenv).

## Installation and Usage

- Clone the repository: git clone [https://github.com/jmvidal26/2_PRODUCTIVITY-AGENT](https://github.com/jmvidal26/2_PRODUCTIVTY-AGENT)

- Install requirements: pip install -r requirements.txt

- Environment Setup:
Create a .env file and add your API key:
GEMINI_API_KEY=your_key_here

Run the application: python core/testing_ui_async.py



## Note:
This is the stable legacy version of the Productivity Agent. A more advanced V3 architecture focusing on 6-hemisphere synchronization and sub-ms latency is currently under development."
