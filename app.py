import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração inicial do banco de dados
def setup_database():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# Função para adicionar uma transação
def add_transaction(type, category, description, amount, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (type, category, description, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (type, category, description, amount, date))
    conn.commit()
    conn.close()

st.title("Gerenciador Financeiro")

# Formulário para inserir transações
with st.form("transaction_form"):
    type = st.selectbox("Tipo", ["Receita", "Despesa"])
    category = st.text_input("Categoria")
    description = st.text_input("Descrição")
    amount = st.number_input("Valor", min_value=0.01)
    date = st.date_input("Data", value=datetime.today())
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        add_transaction(type, category, description, amount, str(date))
        st.success("Transação adicionada com sucesso!")

# Função para buscar transações
def fetch_transactions():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

df = fetch_transactions()

if not df.empty:
    st.subheader("Transações Recentes")
    st.dataframe(df)

    # Gráfico de gastos por categoria
    st.subheader("Distribuição de Gastos")
    category_data = df[df['type'] == "Despesa"].groupby("category")["amount"].sum()
    st.bar_chart(category_data)
