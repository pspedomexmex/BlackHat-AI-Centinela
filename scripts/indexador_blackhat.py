import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# RUTAS ABSOLUTAS (Evitamos errores de puntero)
LIBROS_DIR = "/home/edgar/blackhat_ai/docs"
DB_DIR = "/home/edgar/blackhat_ai/db_vectorial"

# 1. Cargamos el motor de búsqueda (Embeddings)
print("⏳ Cargando motor de búsqueda local...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    model_kwargs={'local_files_only': True}
)

# 2. Leemos todos los manuales de la carpeta
documentos = []
for archivo in os.listdir(LIBROS_DIR):
    if archivo.endswith(".pdf"):
        print(f"📄 Procesando: {archivo}")
        loader = PyMuPDFLoader(os.path.join(LIBROS_DIR, archivo))
        documentos.extend(loader.load())

# 3. Dividimos el texto respetando el contexto
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
fragmentos = text_splitter.split_documents(documentos)

# 4. Creamos la base de datos local
print(f"🧠 Indexando {len(fragmentos)} fragmentos en su 5600G...")
vector_db = Chroma.from_documents(
    documents=fragmentos, 
    embedding=embeddings, 
    persist_directory=DB_DIR
)
print("✅ ¡Vínculo completado! Su IA ya tiene acceso a los libros.")
