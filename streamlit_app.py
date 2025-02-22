import streamlit as st
import re
import json
import time
from datetime import datetime

class BusinessChatbot:
    def __init__(self):
        self.setup_ui()
        self.initialize_state()
        self.load_knowledge_base()
        
    def setup_ui(self):
        st.set_page_config(
            page_title="Assistente Empresarial",
            page_icon="🤖",
            layout="wide"
        )
        
        st.title("🤖 Assistente Empresarial")
        
        # Sidebar para configurações
        with st.sidebar:
            st.header("Configurações")
            st.selectbox("Área de Especialidade", 
                        ["Atendimento ao Cliente", 
                         "Vendas", 
                         "Suporte Técnico"])
            st.checkbox("Modo Debug", key="debug_mode")
    
    def initialize_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "context" not in st.session_state:
            st.session_state.context = {
                "last_intent": None,
                "user_info": {},
                "session_start": datetime.now()
            }
    
    def load_knowledge_base(self):
        self.knowledge_base = {
            "calculos": {
                "soma": lambda x, y: x + y,
                "subtracao": lambda x, y: x - y,
                "multiplicacao": lambda x, y: x * y,
                "divisao": lambda x, y: x / y if y != 0 else "Não é possível dividir por zero"
            },
            "intents": {
                "saudacao": ["oi", "olá", "bom dia", "boa tarde", "boa noite"],
                "despedida": ["tchau", "até logo", "adeus"],
                "calculo": ["quanto é", "calcule", "calcular", "resultado de"],
                "ajuda": ["ajuda", "help", "socorro", "não entendi"]
            },
            "respostas": {
                "saudacao": [
                    "Olá! Sou o assistente empresarial. Como posso ajudar sua empresa hoje?",
                    "Bem-vindo! Estou aqui para auxiliar em suas necessidades empresariais."
                ],
                "despedida": [
                    "Foi um prazer ajudar! Se precisar de mais alguma coisa, é só voltar.",
                    "Até mais! Lembre-se que estou sempre disponível para auxiliar sua empresa."
                ],
                "ajuda": [
                    """Posso ajudar com:
                    1. Análises de dados e relatórios
                    2. Cálculos e projeções
                    3. Atendimento ao cliente
                    4. Suporte técnico
                    5. Automação de processos
                    
                    Como posso te ajudar hoje?"""
                ]
            }
        }
    
    def detect_intent(self, text):
        text = text.lower()
        for intent, patterns in self.knowledge_base["intents"].items():
            if any(pattern in text for pattern in patterns):
                return intent
        return "unknown"
    
    def extract_numbers(self, text):
        numbers = re.findall(r'\d+', text)
        return [float(num) for num in numbers]
    
    def process_calculation(self, text):
        numbers = self.extract_numbers(text)
        if len(numbers) < 2:
            return "Preciso de dois números para fazer o cálculo."
            
        text = text.lower()
        if "mais" in text or "soma" in text:
            return f"O resultado de {numbers[0]} + {numbers[1]} = {self.knowledge_base['calculos']['soma'](numbers[0], numbers[1])}"
        elif "menos" in text or "subtrai" in text:
            return f"O resultado de {numbers[0]} - {numbers[1]} = {self.knowledge_base['calculos']['subtracao'](numbers[0], numbers[1])}"
        elif "vezes" in text or "multiplica" in text:
            return f"O resultado de {numbers[0]} × {numbers[1]} = {self.knowledge_base['calculos']['multiplicacao'](numbers[0], numbers[1])}"
        elif "dividido" in text or "divisão" in text:
            return f"O resultado de {numbers[0]} ÷ {numbers[1]} = {self.knowledge_base['calculos']['divisao'](numbers[0], numbers[1])}"
            
        return "Desculpe, não entendi qual operação você quer realizar."
    
    def generate_response(self, user_input, intent):
        if intent == "calculo":
            return self.process_calculation(user_input)
        elif intent in self.knowledge_base["respostas"]:
            return self.knowledge_base["respostas"][intent][0]
        
        # Processamento mais complexo para outros casos
        return self.process_complex_query(user_input)
    
    def process_complex_query(self, query):
        # Aqui você pode adicionar lógica mais complexa
        # Por exemplo, integração com APIs externas, análise de dados, etc.
        return f"Entendi sua consulta: '{query}'. Como posso ajudar especificamente?"
    
    def update_context(self, user_input, intent):
        st.session_state.context["last_intent"] = intent
        if st.session_state.get("debug_mode", False):
            st.sidebar.write("Debug Info:", {
                "intent": intent,
                "input": user_input,
                "timestamp": datetime.now()
            })
    
    def run(self):
        # Mostrar histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        if user_input := st.chat_input("Como posso ajudar sua empresa hoje?"):
            # Processar input
            intent = self.detect_intent(user_input)
            self.update_context(user_input, intent)
            
            # Mostrar mensagem do usuário
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Gerar e mostrar resposta
            with st.spinner("Processando..."):
                response = self.generate_response(user_input, intent)
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chatbot = BusinessChatbot()
    chatbot.run()
