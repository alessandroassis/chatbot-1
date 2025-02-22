import streamlit as st
import random
import time
import re

class Chatbot:
    def __init__(self):
        self.setup_ui()
        self.initialize_state()
        self.respostas = {
            "oi": ["Olá! Como posso ajudar?", "Oi! Em que posso ser útil?"],
            "bom dia": ["Bom dia! Como posso ajudar?", "Bom dia! Em que posso ser útil hoje?"],
            "boa tarde": ["Boa tarde! Como posso ajudar?", "Boa tarde! Em que posso ser útil hoje?"],
            "boa noite": ["Boa noite! Como posso ajudar?", "Boa noite! Em que posso ser útil hoje?"],
            "ajuda": ["Posso ajudar com:\n- Cálculos matemáticos\n- Dúvidas gerais\n- Análise de textos"],
            "tchau": ["Até mais! Foi um prazer ajudar!", "Tchau! Volte sempre!"],
        }
        
    def setup_ui(self):
        st.title("🤖 Assistente IA")
        st.markdown("""
        ### Bem-vindo ao seu assistente!
        Posso ajudar com:
        - Cálculos matemáticos
        - Dúvidas gerais
        - Análise de textos
        """)
        
    def initialize_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def calculate_mil_vezes(self, numero):
        try:
            num = float(numero)
            resultado = num * 1000
            return f"O resultado de {num} × 1000 = {resultado:,.2f}"
        except:
            return "Desculpe, não consegui entender o número para calcular."
    
    def process_math_question(self, text):
        # Procura por padrões de "quanto é X vezes mil"
        mil_pattern = r"quanto.*?(\d+).*?mil"
        if match := re.search(mil_pattern, text.lower()):
            return self.calculate_mil_vezes(match.group(1))
            
        # Outros padrões matemáticos podem ser adicionados aqui
        return None
    
    def get_bot_response(self, user_input):
        # Simula processamento
        time.sleep(0.5)
        
        # Verifica se é uma questão matemática
        if math_response := self.process_math_question(user_input):
            return math_response
        
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
