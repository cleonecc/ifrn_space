import openai
from PyPDF2 import PdfReader
import streamlit as st

# Configurar a API do OpenAI
openai.api_key = "SUA_CHAVE_API"

# Função para extrair texto do PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Função para perguntar ao modelo GPT
def ask_gpt(question, context):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Use o contexto abaixo para responder à pergunta de forma clara e direta.\n\nContexto:\n{context}\n\nPergunta: {question}\nResposta:",
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response["choices"][0]["text"].strip()

# Interface do usuário com Streamlit
def main():
    st.title("Chatbot que Aprende de um PDF")
    st.write("Faça upload de um arquivo PDF e interaja com o conteúdo dele!")

    # Carregar PDF
    uploaded_file = st.file_uploader("Faça upload do seu PDF", type="pdf")
    
    if uploaded_file:
        with st.spinner("Extraindo texto do PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success("Texto extraído com sucesso!")

        # Mostre uma prévia do conteúdo do PDF
        with st.expander("Mostrar conteúdo do PDF"):
            st.write(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)

        # Entrada de pergunta
        question = st.text_input("Digite sua pergunta sobre o conteúdo do PDF:")
        if question:
            with st.spinner("Gerando resposta..."):
                answer = ask_gpt(question, pdf_text)
                st.write("### Resposta:")
                st.write(answer)

if __name__ == "__main__":
    main()
