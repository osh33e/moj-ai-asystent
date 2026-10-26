import streamlit as st
import google.generativeai as genai

# Konfiguracja wyglądu aplikacji
st.set_page_config(page_title="AI Game Dev Assistant", page_icon="🕹️", layout="centered")
st.title("🕹️ Twój Asystent Gamedev")
st.caption("Ekspert od Skript, modów Minecraft i apek C# (np. custom crosshairs, launchery)")

# Pobieranie klucza API z zabezpieczeń chmury
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# Konfiguracja mózgu AI (szybki model z dostępem do wiedzy)
model = genai.GenerativeModel('gemini-2.5-flash')

# Zdefiniowanie roli dla AI
SYSTEM_PROMPT = """Jesteś zaawansowanym architektem oprogramowania i programistą. 
Twoim celem jest pisanie i poprawianie:
- Skryptów (Skript plugin) do Minecrafta na zaawansowane serwery.
- Kodu w C# do tworzenia aplikacji takich jak nakładki z celownikiem czy własne launchery.
Masz pisać gotowy kod i tłumaczyć krok po kroku, jak go zaimplementować. Pisz zwięźle."""

# Pamięć sesji (żeby aplikacja pamiętała historię czatu)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie poprzednich wiadomości
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Pole tekstowe dla Ciebie
prompt = st.chat_input("Co dzisiaj programujemy?")
if prompt:
    # Wyświetlenie Twojego zapytania
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Reakcja AI
    with st.chat_message("assistant"):
        with st.spinner("Piszę kod..."):
            try:
                # Wysłanie zapytania wraz z rolą systemową
                pelne_zapytanie = f"{SYSTEM_PROMPT}\n\nUżytkownik pisze: {prompt}"
                odpowiedz = model.generate_content(pelne_zapytanie)
                
                # Wyświetlenie wygenerowanego kodu
                st.markdown(odpowiedz.text)
                st.session_state.messages.append({"role": "assistant", "content": odpowiedz.text})
            except Exception as e:
                st.error(f"Błąd połączenia: {e}")
