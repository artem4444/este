# main/streamlit_apps/user_chat.py
import streamlit as st

class UserChat:
    @staticmethod
    def render_huggingface_chat(container):
        """
        Embed Hugging Face chat in a Streamlit container
        
        Args:
            container (st.container): Streamlit container to embed chat
        """
        with container:
            st.header("💬 Hugging Face Chat")
            
            # Embed Hugging Face chat with custom styling
            st.markdown("""
            <style>
            .hf-chat-container {
                width: 100%;
                height: 600px;
                border: none;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.components.v1.html('''
                <iframe 
                    src="https://huggingface.co/chat" 
                    width="100%" 
                    height="600" 
                    class="hf-chat-container"
                    frameborder="0"
                ></iframe>
            ''', height=600, scrolling=True)

def main():
    # Demonstration of how to use the UserChat module
    st.set_page_config(layout="wide")
    
    # Create columns
    left_col, right_col = st.columns([1, 3])
    
    # Render chat in left column
    UserChat.render_huggingface_chat(left_col)

if __name__ == "__main__":
    main()