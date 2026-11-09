import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURACIÓN DE RUTAS RELATIVAS ---
# Definimos la base como la carpeta raíz del proyecto (un nivel arriba de /scripts)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_PATH = os.path.join(BASE_DIR, "docs")
DB_PATH = os.path.join(BASE_DIR, "db_vectorial")

def generar_base_datos():
    print(f"🔍 Buscando manuales en: {DOCS_PATH}...")
    
    if not os.path.exists(DOCS_PATH) or not os.listdir(DOCS_PATH):
        print("❌ Error: La carpeta 'docs' está vacía o no existe.")
        return

    # 1. Cargador de Directorio (Busca todos los PDFs en /docs)
    loader = DirectoryLoader(DOCS_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    documentos = loader.load()
    print(f"📄 Se cargaron {len(documentos)} páginas de manuales.")

    # 2. Divisor de texto (Chunking)
    # Ajustado para mantener el contexto técnico de los comandos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    fragmentos = text_splitter.split_documents(documentos)
    print(f"✂️ Documentos divididos en {len(fragmentos)} fragmentos técnicos.")

    # 3. Modelo de Embeddings (Carga Local para el Ryzen 5600G)
    print("🧠 Generando vectores (esto puede tardar unos minutos)...")
    # Nota: el primer arranque descarga el modelo de embeddings (~1 GB) desde HuggingFace.
    # Despues queda en cache y el sistema funciona 100% local/offline.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )

    # 4. Creación y Persistencia de la DB en /db_vectorial
    vector_db = Chroma.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"✅ ¡Éxito! Base de datos creada y guardada en: {DB_PATH}")

if __name__ == "__main__":
    generar_base_datos()
