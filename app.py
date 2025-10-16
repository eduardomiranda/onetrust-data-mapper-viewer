import streamlit as st
from pymongo import MongoClient
import json

# =========================
# Configuração e conexão
# =========================
@st.cache_resource
def get_db():
    try:
        # Lê o segredo armazenado em .streamlit/secrets.toml
        uri = st.secrets["MONGODB_URI"]
        client = MongoClient(uri)
        db = client["onetrust_scrapper_brasilseg"]
        return db
    except KeyError:
        st.error("❌ MONGODB_URI não encontrado em secrets.toml. Verifique a configuração.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao MongoDB: {e}")
        st.stop()

# Inicializa conexão
db = get_db()
collection = db["data_mapping_automation"]

# =========================
# Layout Streamlit
# =========================
st.set_page_config(page_title="Data Mapping Automation - MongoDB Viewer", layout="wide")

st.title("📊 Data Mapping Automation - MongoDB Viewer")
st.write("Visualização dos dados da collection `data_mapping_automation` do banco `onetrust_scrapper_brasilseg`.")

# =========================
# Consultas no MongoDB
# =========================
try:
    col1, col2 = st.columns(2)

    with col1:
        total_docs = collection.count_documents({})
        st.metric("Total de documentos", total_docs)

    with col2:
        total_validados = collection.count_documents({"validado": True})
        st.metric("Total de documentos validados", total_validados)


    # Botão para carregar os dados (evita sobrecarga)
    if st.button("🔍 Carregar dados da coleção"):
        data = list(collection.find({}, {"_id": 0}))  # Remove o campo _id para visualização
        if data:
            st.subheader("📄 Dados em formato JSON")
            st.json(data, expanded=False)
        else:
            st.warning("A coleção está vazia.")
except Exception as e:
    st.error(f"Erro ao acessar a coleção: {e}")
