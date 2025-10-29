import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def get_db():
    try:
        if not firebase_admin._apps:
            cred_info = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_info)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"Erro ao conectar ao Firestore: {e}")
        st.stop()
