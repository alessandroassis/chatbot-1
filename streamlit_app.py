import streamlit as st
import random
import time

# Configuração da página
st.set_page_config(
    page_title="Assistente IA",
    page_icon="🤖",
    layout="centered"
)

class Chatbot:
    def __init__(self):
        self.setup_ui()
        self.initialize_state()
        self.respostas = {
            "oi": ["Olá! Como posso ajudar?", "Oi! Em que posso ser útil?", "Olá! O que você precisa?"],
            "bom dia": ["Bom dia! Como posso ajudar?", "Bom dia! Em que posso ser útil hoje?"],
            "boa tarde": ["Boa tarde! Como posso ajudar?", "Boa tarde! Em que posso ser útil hoje?"],
            "boa noite": ["Boa noite! Como posso ajudar?", "Boa noite! Em que posso ser útil hoje?"],
            "ajuda": ["Posso ajudar com:\n- Dúvidas gerais\n- Análise de textos\n- Sugestões e recomendações"],
            "quem é você": ["Sou um assistente virtual criado para ajudar em diversas tarefas!"],
            "tchau": ["Até mais! Foi um prazer ajudar!", "Tchau! Volte sempre!"],
        }
        
    def setup_ui(self):
        st.title("🤖 Assistente IA")
        st.markdown("""
        ### Bem-vindo ao seu assistente!
        Posso ajudar com:
        - Dúvidas gerais
        - Análise de textos
        - Sugestões e recomendações
        """)
        
    def initialize_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def get_bot_response(self, user_input):
        # Simula processamento
        time.sleep(0.5)
        
        # Converte input para minúsculas para comparação
        user_input_lower = user_input.lower()
        
        # Verifica se há resposta predefinida
        for key in self.respostas:
            if key in user_input_lower:
                return random.choice(self.respostas[key])
        
        # Resposta genérica para outros casos
        return f"Entendi sua mensagem: '{user_input}'. Como posso ajudar mais?"
    
    def display_message(self, content, role):
        with st.chat_message(role):
            st.markdown(content)
    
    def run(self):
        # Mostra histórico
        for message in st.session_state.messages:
            self.display_message(message["content"], message["role"])
        
        # Input do usuário
        if user_input := st.chat_input("Digite sua mensagem..."):
            # Mostra mensagem do usuário
            self.display_message(user_input, "user")
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Gera e mostra resposta
            with st.spinner("Pensando..."):
                response = self.get_bot_response(user_input)
                self.display_message(response, "assistant")
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
