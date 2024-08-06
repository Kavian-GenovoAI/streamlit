import streamlit as st

st.title("Support Helper Demonstration")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "printer_selected" not in st.session_state:
    st.session_state.printer_selected = None
if "issue_selected" not in st.session_state:
    st.session_state.issue_selected = None


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def is_printer_related(message):
    printer_keywords = ["printer", "print", "printing", "ink", "cartridge"]
    return any(keyword in message.lower() for keyword in printer_keywords)


if prompt := st.chat_input("What is up?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    if is_printer_related(prompt):
        response_content = """
        Analytics: 😞 | 🤖 | 🛠 | 🖨️\n
        **Please Select your printer:**
        """
        with st.chat_message("bot"):
            st.markdown(response_content)
            cols = st.columns(3)
            printers = ['Pro', 'Pro S', 'Pro 2']

            def select_printer(printer):
                st.session_state.printer_selected = printer
                st.session_state.messages.append({"role": "bot", "content": f"You selected {printer}"})
                st.session_state.messages.append({"role": "bot", "content": "Here are some of the top choices. What would you like help with?"})

            for i, printer in enumerate(printers):
                with cols[i]:
                    st.button(printer, on_click=select_printer, args=(printer,))


if st.session_state.printer_selected:
    issue_cols = st.columns(4)
    issues = ["Printer offline", "WiFi", "Cartridge errors", "Paper jam"]

    def select_issue(issue):
        st.session_state.issue_selected = issue
        st.session_state.messages.append({"role": "user", "content": issue})
        if issue == "Cartridge errors":
            st.session_state.messages.append({"role": "bot", "content": "I can help with cartridge errors. Is your printer enrolled in Instant Ink?"})
            ink_options = ["Yes", "No", "What is Instant Ink?"]
            ink_cols = st.columns(len(ink_options))

            def select_ink_option(option):
                st.session_state.messages.append({"role": "user", "content": option})

            for k, option in enumerate(ink_options):
                with ink_cols[k]:
                    st.button(option, on_click=select_ink_option, args=(option,))

    for j, issue in enumerate(issues):
        with issue_cols[j]:
            st.button(issue, on_click=select_issue, args=(issue,))




