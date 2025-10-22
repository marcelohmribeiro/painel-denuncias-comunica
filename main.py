import streamlit as st
import pandas as pd
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, firestore

def get_db():
    if not firebase_admin._apps:
        cred_info = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_info)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def load_flat_df(collection: str) -> pd.DataFrame:
    db = get_db()
    q = db.collection(collection).select([
        "category",
        "location",
        "createdAt",
        "updatedAt"
    ])

    docs = list(q.stream())
    rows = []
    for d in docs:
        rec = d.to_dict() or {}
        rec["id"] = d.id
        rows.append(rec)

    if not rows:
        return pd.DataFrame()

    flat = pd.json_normalize(rows, sep=".")
    return flat

def main():
    st.set_page_config(page_title="Comunica", layout="wide")
    st.markdown("## Painel Global de Denúncias")

    df = load_flat_df("reports")
    lista_colunas = {
        "category": "Categoria",
        "location.address.street": "Rua",
        "location.address.district": "Bairro",
        "location.address.city": "Cidade",
        "location.address.region": "Estado",
        "createdAt": "Criado em",
        "updatedAt": "Atualizado em"
    }

    df_label = df.rename(columns=lista_colunas)

    colunas = list(lista_colunas.values())
    selecionadas = st.multiselect("Selecione as colunas que deseja visualizar:", colunas, default=colunas)
    st.dataframe(df_label[selecionadas], height=500)

    st.divider()

    st.markdown("### Contagem por Bairro")
    col_district = "location.address.district"

    counts = df[col_district].value_counts()

    col1, col2 = st.columns(2, gap="large", border=True)
    
    counts_df = counts.reset_index()
    counts_df.columns = ["district", "count"]

    with col1:
        fig = px.bar(
            counts_df,
            x="district", 
            y="count",
            title="Contagem por Bairro",
            labels={"district": "Bairro", "count": "Contagem"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            counts_df,
            names="district",
            values="count",
            title="Proporção por Bairro"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()

    if "location.coordinate.latitude" in df.columns and "location.coordinate.longitude" in df.columns:
        st.markdown("### Mapa das Denúncias")
        df_mapa = df.rename(
        columns={
            "location.coordinate.latitude": "lat",
            "location.coordinate.longitude": "lon"
        }
    )
        st.map(df_mapa[["lat", "lon"]], zoom=11)
    else:
        st.warning("Não há coordenadas de latitude/longitude nos dados.")

if __name__ == "__main__":
    main()
