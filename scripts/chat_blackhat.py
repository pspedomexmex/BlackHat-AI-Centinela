import os
import sys
# Asegúrese de tener instalado: pip install -U langchain-ollama langchain-chroma langchain-huggingface
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONFIGURACIÓN DE INTERFAZ (ANSI) ---
C_QUERY = "\033[1;36m"  # Cian (Consultas del Operador)
C_RESP  = "\033[1;32m"  # Verde (Teoría de los Manuales)
C_INFO  = "\033[1;33m"  # Amarillo (Código y Metadatos)
C_RESET = "\033[0m"     # Reset de Color

# 1. Configuración del LLM (Optimizado para iGPU con 2GB VRAM)
# Temperature=0 para máxima precisión y cero creatividad/alucinación
llm = OllamaLLM(model="phi3:mini", temperature=0)

# 2. Motor de Embeddings (Carga Local)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={'local_files_only': True}
)

# 3. Conexión a la Base de Datos Vectorial (36,140 Fragmentos)
DB_PATH = "../db_vectorial"

if not os.path.exists(DB_PATH):
    print(f"{C_INFO}❌ ERROR: No se encontró la base de datos en {DB_PATH}{C_RESET}")
    sys.exit(1)

vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

def centinela_blackhat(pregunta):
    # k=4 para permitir correlación cruzada entre manuales teóricos y prácticos
    docs = vector_db.similarity_search(pregunta, k=4)
    
    fuentes = set([os.path.basename(d.metadata.get('source', 'Manual')) for d in docs])
    contexto = "\n".join([d.page_content for d in docs])
    
    # PROMPT DE AUDITORÍA ESTRICTA
    prompt = f"""### SISTEMA DE AUDITORÍA TÉCNICA - MODO EXCLUSIVIDAD LOCAL ###
    ACTÚA COMO UN AUDITOR DE SEGURIDAD. RESPONDE SIEMPRE EN ESPAÑOL.
    
    REGLA DE ORO DE INTEGRIDAD:
    - Si la información solicitada NO está en el CONTEXTO LOCAL, responde: 
      "Información no encontrada en los manuales locales indexados."
    - Prohibido usar conocimientos externos o inventar herramientas/comandos.
    - El código debe seguir fielmente los ejemplos de las fuentes citadas.
    
    CONTEXTO LOCAL:
    {contexto}
    
    PREGUNTA: {pregunta}
    
    RESPUESTA:"""
    
    print(f"\n{C_INFO}📚 FUENTES IDENTIFICADAS: {list(fuentes)}{C_RESET}")
    print(f"{C_RESP}💀 RESPUESTA AUDITADA:{C_RESET}")
    
    dentro_de_codigo = False
    sys.stdout.write(C_RESP) # Empezar en verde para la teoría
    
    # Procesamiento por streaming para reducir latencia en el 5600G
    for chunk in llm.stream(prompt):
        if "```" in chunk:
            dentro_de_codigo = not dentro_de_codigo
            # Amarillo para código, Verde para texto
            color_actual = C_INFO if dentro_de_codigo else C_RESP
            sys.stdout.write(color_actual + chunk)
        else:
            sys.stdout.write(chunk)
        
        sys.stdout.flush()
    
    sys.stdout.write(C_RESET + "\n")

# --- BUCLE PRINCIPAL ---
print(f"\n{C_INFO}=== CENTINELA BLACK HAT v4.5 (STRICT AUDIT MODE) ==={C_RESET}")
print(f"{C_INFO}Optimizado para: Ryzen 5 5600G | Filtro: Honestidad Total{C_RESET}")

while True:
    try:
        query = input(f"\n{C_QUERY}🔍 CONSULTA TÉCNICA: {C_RESET}")
        if query.lower() in ['salir', 'exit', 'quit']:
            print(f"{C_INFO}🛑 Cerrando sesión de auditoría...{C_RESET}")
            break
        if query.strip():
            centinela_blackhat(query)
    except KeyboardInterrupt:
        print(f"\n{C_INFO}🛑 Interrupción de seguridad.{C_RESET}")
        break
