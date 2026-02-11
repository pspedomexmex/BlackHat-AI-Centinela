# 💀 Black Hat AI - Centinela de Auditoría Técnica (v4.5)

**Estado del proyecto:** 🟢 Beta / En desarrollo inicial.

Este proyecto es una herramienta de apoyo para estudiantes y profesionales de **Ingeniería en Sistemas** y Ciberseguridad. Utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** para realizar consultas técnicas precisas sobre manuales de auditoría locales, optimizando el rendimiento en hardware de consumo como el **AMD Ryzen 5 5600G**.

## ⚠️ Advertencias Legales y Éticas
- **Uso Ético:** Esta herramienta ha sido diseñada exclusivamente con fines educativos y de auditoría autorizada. El mal uso de la información generada es responsabilidad total del usuario.
- **Derechos de Autor:** Este repositorio NO incluye los manuales técnicos (PDFs) ni la base de datos vectorial pre-cargada debido a restricciones de propiedad intelectual.
- **Sobre la Bibliografía:** El sistema es agnóstico; usted puede indexar sus propios manuales de certificación (EC-Council, LPI, Offensive Security, etc.). Si desea conocer la lista de materiales utilizados en mis pruebas o tiene dudas sobre cómo obtenerlos respetando los derechos de autor, puede enviarme un mensaje directo para orientarle sobre las fuentes oficiales.

## 🚀 Características Principales
- **Filtro de Honestidad:** El sistema está programado para no alucinar. Si el dato no existe en su biblioteca local, admitirá ignorancia en lugar de inventar comandos.
- **Interfaz Visual:** Diferenciación por colores ANSI (Verde para teoría, Amarillo para código, Cian para el operador).
- **Privacidad Total:** Todo se ejecuta de forma local mediante **Ollama (Phi-3:mini)**. No se envían datos a la nube.

## 🛠️ Requisitos del Sistema y Configuración

Para que el **Centinela v4.5** funcione correctamente en su entorno local, siga este orden de instalación:

### 1. Instalación del Motor de IA (Ollama)
Este proyecto utiliza **Ollama** como motor de inferencia local para garantizar la soberanía de los datos.

* **Instalar en Linux (Kali/Ubuntu/Debian):**

      curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
  
Descargar el modelo técnico: Utilizamos phi3:mini por su excelente equilibrio entre precisión técnica y bajo consumo de recursos (ideal para los 2GB de VRAM de la iGPU del Ryzen 5600G).

    ollama pull phi3:mini



### 2. Preparación del Entorno Python
Se recomienda el uso de un entorno virtual (Conda o venv).



### 3. Instalar dependencias
    pip install -r config/requirements.txt



#### 4. arga de Conocimiento (Indexación)
Para alimentar la base de datos con sus propios manuales:
Coloque sus archivos PDF en la carpeta docs/.
Ejecute el script procesador desde la raíz:

    python3 scripts/indexador_blackhat.py
Esto generará la carpeta db_vectorial/ en la raíz del proyecto.


### 5. Ejecución del Auditor Centinela
Una vez indexados los documentos, inicie la interfaz de consulta:

    python3 scripts/chat_blackhat.py  


📋 Metodología de Uso
Consulta Técnica: Realice preguntas sobre protocolos, vulnerabilidades o comandos específicos.

Respuesta Auditada: El sistema buscará en sus manuales locales. Si la información no está presente, el filtro de integridad le informará que no hay evidencia documental.

Código Seguro: Los fragmentos de código se resaltarán en amarillo para diferenciarlos de la teoría (verde).

Desarrollado por Edgar - Ingeniería en Sistemas 2026
