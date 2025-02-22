import streamlit as st

st.title("Chatbot Simples")

# Inicializa o histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra o histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de input
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Resposta do bot (simplificada)
    response = f"Você disse: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
