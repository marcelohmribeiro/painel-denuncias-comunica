import streamlit as st
import plotly.express as px
from modules.reports import load_flat_df


def reports():
    st.title("Painel Global de Denúncias")

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
    st.dataframe(df_label[selecionadas])

    st.divider()

    st.subheader("Contagem por Bairro")
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
        st.subheader("Mapa das Denúncias")
        df_mapa = df.rename(
        columns={
            "location.coordinate.latitude": "lat",
            "location.coordinate.longitude": "lon"
        }
    )
        st.map(df_mapa[["lat", "lon"]], zoom=11)
    else:
        st.warning("Não há coordenadas de latitude/longitude nos dados.")

