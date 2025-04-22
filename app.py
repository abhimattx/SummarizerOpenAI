import streamlit as st
import os
import base64
from openai_api import summarize_text, summarize_file, count_tokens, estimate_cost
from file_handler import extract_text_from_file, get_file_preview, extract_text_from_file_with_metadata

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('assets', exist_ok=True)

st.set_page_config(page_title="GPT Summarizer", layout="wide")
st.title("📄 GPT Summarizer")

# Initialize session state for token tracking
if 'token_count' not in st.session_state:
    st.session_state.token_count = 0
if 'estimated_cost' not in st.session_state:
    st.session_state.estimated_cost = 0.0

# Sidebar settings
st.sidebar.title("Settings")

# Model selection in sidebar
model_option = st.sidebar.selectbox(
    "Select GPT Model",
    ["gpt-3.5-turbo", "gpt-4"],
    help="GPT-4 is more capable but costs more"
)

# API key input in sidebar
use_custom_key = st.sidebar.checkbox("Use your own OpenAI API Key")
if use_custom_key:
    openai_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
else:
    openai_key = st.secrets.get("OPENAI_API_KEY")

# Display token usage stats in sidebar
st.sidebar.title("Usage Statistics")
st.sidebar.metric("Tokens Used", f"{st.session_state.token_count}")
st.sidebar.metric("Estimated Cost", f"${st.session_state.estimated_cost:.5f}")
st.sidebar.info("Costs are approximate and based on OpenAI's pricing")

# Reset button in sidebar
if st.sidebar.button("Get Statistics"):
    st.session_state.token_count = 0
    st.session_state.estimated_cost = 0.0
    st.sidebar.success("Statistics!")

# Tabs for different input types
tab1, tab2 = st.tabs(["Text Summarization", "File Summarization"])

with tab1:
    st.markdown("Summarize any text using OpenAI's GPT models. Paste text below and choose a summary length.")
    text_input = st.text_area("Enter your text:", height=300)
    summary_type = st.radio("Summary Length", ["Short", "Medium", "Long"], horizontal=True)
    
    if st.button("Generate Text Summary"):
        if not text_input.strip():
            st.warning("Please enter some text.")
        elif not openai_key:
            st.error("No OpenAI API key provided.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    # Count tokens before request
                    input_tokens = count_tokens(text_input)
                    
                    # Generate summary
                    summary, response_tokens = summarize_text(
                        text_input, 
                        summary_type.lower(), 
                        openai_key, 
                        model=model_option,
                        return_tokens=True
                    )
                    
                    # Update token count and cost in session state
                    total_tokens = input_tokens + response_tokens
                    st.session_state.token_count += total_tokens
                    st.session_state.estimated_cost += estimate_cost(total_tokens, model_option)
                    
                    # Display summary
                    summary, usage = summarize_text(text_input, summary_type.lower(), openai_key)
                    st.subheader("📝 Summary")
                    st.write(summary)

                    # Token info
                    st.info(f"🔢 Prompt Tokens: {usage.prompt_tokens} | Completion Tokens: {usage.completion_tokens} | Total: {usage.total_tokens}")

                    # Cost estimation
                    cost_per_1k = 0.0015  # For GPT-3.5-turbo input + output
                    estimated_cost = (usage.total_tokens / 1000) * cost_per_1k
                    st.caption(f"💰 Estimated Cost: ${estimated_cost:.5f}")

                    
                    # Option to download summary
                    st.download_button(
                        "Download Summary",
                        summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.markdown("Upload a document (PDF, DOCX, or TXT) to generate a summary.")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    
    summary_type = st.radio("File Summary Length", ["Short", "Medium", "Long"], horizontal=True, key="file_summary_length")
    
    if uploaded_file is not None:
        st.info(f"File uploaded: {uploaded_file.name}")
        
        # File preview section
        preview_col1, preview_col2 = st.columns([1, 2])
        
        with preview_col1:
            # Display file metadata and thumbnail
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext == '.pdf':
                st.markdown("### PDF Document")
                preview_img = get_file_preview(uploaded_file)
                if preview_img:
                    st.image(preview_img, width=300, caption=f"First page preview: {uploaded_file.name}")
                    
            elif file_ext == '.docx':
                st.markdown("### Word Document")
                st.image("https://img.icons8.com/color/96/000000/microsoft-word-2019--v2.png", width=100)
            
            elif file_ext == '.txt':
                st.markdown("### Text File")
                st.image("https://img.icons8.com/color/96/000000/text-file.png", width=100)

        with preview_col2:
            # Extract and display text preview
            try:
                metadata, file_text = extract_text_from_file_with_metadata(uploaded_file)
                
                # Show metadata if available
                if metadata:
                    with st.expander("File Metadata", expanded=True):
                        for key, value in metadata.items():
                            if value and str(value).strip():
                                st.write(f"**{key}:** {value}")
                
                # Show text preview
                if file_text and len(file_text) > 0:
                    with st.expander("File Content Preview", expanded=True):
                        st.text_area("Content", file_text[:3000] + ("..." if len(file_text) > 3000 else ""), 
                                    height=300, disabled=True)
                else:
                    st.warning("No text content could be extracted for preview.")
                    
            except Exception as e:
                st.error(f"Preview error: {str(e)}")
        
        if st.button("Generate File Summary"):
            if not openai_key:
                st.error("No OpenAI API key provided.")
            else:
                with st.spinner("Extracting text and generating summary..."):
                    try:
                        # Extract text from the file
                        file_text = extract_text_from_file(uploaded_file)
                        
                        if file_text and len(file_text) > 0:
                            # Count tokens before request
                            input_tokens = count_tokens(file_text[:9000])  # Only count what we'll send
                            
                            # Generate summary
                            summary, response_tokens = summarize_file(
                                file_text, 
                                uploaded_file.name, 
                                summary_type.lower(), 
                                openai_key,
                                model=model_option,
                                return_tokens=True
                            )
                            
                            # Update token count and cost
                            total_tokens = input_tokens + response_tokens
                            st.session_state.token_count += total_tokens
                            st.session_state.estimated_cost += estimate_cost(total_tokens, model_option)
                            
                            # Display summary
                            st.subheader("📝 Summary")
                            st.write(summary)
                            
                            # Option to download summary
                            st.download_button(
                                "Download Summary",
                                summary,
                                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_summary.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error("Could not extract text from the file. Is it a valid document?")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI GPT API.")
st.markdown("Made with ❤️ by Abhishek Singh")