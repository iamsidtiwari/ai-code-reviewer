import streamlit as st
import os
from agent.pipeline import run_review_pipeline
from utils.formatter import format_reviews_as_markdown
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

st.title("🤖 AI Code Review Agent")

# Sidebar for filters
st.sidebar.header("Filter Results")
severity_filter = st.sidebar.multiselect(
    "Severity",
    ["low", "medium", "high"],
    default=["low", "medium", "high"]
)
category_filter = st.sidebar.multiselect(
    "Category",
    ["security", "performance", "style", "correctness", "maintainability"],
    default=["security", "performance", "style", "correctness", "maintainability"]
)

repo_url = st.text_input("Enter GitHub Repository URL (e.g., https://github.com/user/repo):")

if st.button("Run Review", type="primary"):
    if not repo_url:
        st.error("Please enter a valid GitHub repository URL.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is not set in the .env file.")
    else:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(message, percent):
                status_text.text(message)
                progress_bar.progress(percent / 100.0)
                
            with st.spinner("Pipeline running..."):
                reviews = run_review_pipeline(repo_url, progress_callback=update_progress)
                
            st.success(f"Review complete! Found {len(reviews)} potential issues.")
            st.session_state['reviews'] = reviews
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if 'reviews' in st.session_state:
    reviews = st.session_state['reviews']
    
    # Filter reviews
    filtered_reviews = [
        r for r in reviews 
        if r.get("severity", "").lower() in severity_filter and 
           r.get("category", "").lower() in category_filter
    ]
    
    if not filtered_reviews:
        st.info("No issues found matching the current filters.")
    else:
        # Separate by confidence
        high_conf_reviews = [r for r in filtered_reviews if r.get("confidence", 0) >= 70]
        low_conf_reviews = [r for r in filtered_reviews if r.get("confidence", 0) < 70]
        
        st.subheader("High Confidence Issues")
        for review in high_conf_reviews:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Issue:** {review.get('issue')}")
                    st.markdown(f"**Suggestion:** {review.get('suggestion')}")
                    
                    chunk = review.get('chunk', {})
                    if chunk:
                        with st.expander("View Code Context"):
                            st.code(chunk.get('code'), language="python")
                            
                with col2:
                    severity = review.get("severity", "unknown").lower()
                    color = "red" if severity == "high" else "orange" if severity == "medium" else "green"
                    st.markdown(f"**Severity:** :{color}[{severity.upper()}]")
                    st.markdown(f"**Category:** {review.get('category')}")
                    
                    confidence = review.get("confidence", 0)
                    st.progress(confidence / 100.0, text=f"Confidence: {confidence}%")
        
        if low_conf_reviews:
            with st.expander("⚠️ Verify These (Low Confidence)", expanded=False):
                for review in low_conf_reviews:
                    with st.container(border=True):
                        st.markdown(f"**Issue:** {review.get('issue')}")
                        st.markdown(f"**Suggestion:** {review.get('suggestion')}")
                        st.progress(review.get("confidence", 0) / 100.0, text=f"Confidence: {review.get('confidence', 0)}%")
                        
        # Download button
        md_content = format_reviews_as_markdown(filtered_reviews)
        st.download_button(
            label="Download as Markdown",
            data=md_content,
            file_name="code_review_report.md",
            mime="text/markdown"
        )
