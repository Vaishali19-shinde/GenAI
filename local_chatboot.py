import streamlit as st
import ollama

# Page layout and title configuration
st.set_page_config(page_title="Ollama Web UI", page_icon="🤖", layout="centered")
st.title("🤖 Local Ollama Chatbot")

# Model selection in the sidebar
model_choice = st.sidebar.selectbox(
    "Select Model",
    options=["llama3", "mistral", "gemma", "phi3"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.write("Ensure Ollama is running locally via `ollama serve`.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from context
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask anything..."):
    # Display user message in UI
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Query Ollama with streaming enabled
            stream = ollama.chat(
                model=model_choice,
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in stream:
                full_response += chunk["message"]["content"]
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}")
            full_response = "Sorry, I encountered an error connecting to the model."

    # Store assistant response in history
    st.session_state.messages.append({"role": "assistant", "content": full_response})