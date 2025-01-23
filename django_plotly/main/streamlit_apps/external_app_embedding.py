import streamlit as st

def main():
    st.title("External App Embedding")
    
    # Method 1: Basic iframe embedding
    st.components.v1.iframe(
        src="https://example.com/player", 
        width=800, 
        height=600
    )

    # Method 2: HTML embedding with more control
    st.markdown('''
        <iframe 
            src="https://example.com/player" 
            width="100%" 
            height="600" 
            frameborder="0"
        ></iframe>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()