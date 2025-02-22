# requirements.txt
streamlit==1.31.0
transformers==4.37.2
torch==2.1.2
accelerate==0.27.2

# .streamlit/config.toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

# streamlit_app.py
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class AssistenteIA:
    def __init__(self):
        self.model_name = "facebook/blenderbot-400M-distill"
        self.setup_page()
        self.initialize_state()
        self.run_chat()

    def setup_page(self):
        st.set_page_config(
            page_title="Assistente IA",
            page_icon="🤖",
            layout="wide"
        )
        st.title("🤖 Assistente IA Personalizado")
        st.markdown("""
        ### Bem-vindo ao seu assistente virtual!
        Este assistente pode ajudar com:
        - Dúvidas gerais
        - Análise de textos
        - Sugestões e recomendações
        """)

    @st.cache_resource
    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(self.model_name)
        return tokenizer, model

    def initialize_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "model_loaded" not in st.session_state:
            self.tokenizer, self.model = self.load_model()
            st.session_state.model_loaded = True

    def generate_response(self, prompt):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            return f"Desculpe, ocorreu um erro: {str(e)}"

    def run_chat(self):
        # Mostrar histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input do usuário
        if prompt := st.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gerar e mostrar resposta
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = self.generate_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

if __name__ == "__main__":
    AssistenteIA()
