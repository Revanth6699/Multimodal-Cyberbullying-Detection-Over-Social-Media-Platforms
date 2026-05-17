import streamlit as st
import requests
import matplotlib.pyplot as plt
from collections import Counter

API_ANALYZE = "http://127.0.0.1:8000/analyze"
API_ADD = "http://127.0.0.1:8000/add_word"
API_DELETE = "http://127.0.0.1:8000/delete_word"

st.set_page_config(page_title="Cyberbullying Dashboard", layout="wide")

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
# 🛡️ Cyberbullying Moderation Dashboard
Real-time analysis for Text, Audio, Video & URLs
---
""")

# ==========================================================
# TABS
# ==========================================================

tab1, tab2 = st.tabs(["🔍 Analyze", "⚙️ Manage Words"])

# ==========================================================
# TAB 1: ANALYSIS
# ==========================================================

with tab1:

    input_type = st.radio(
        "Select Input Type",
        ["Text", "File Upload", "URL"],
        horizontal=True
    )

    text_input = None
    file_input = None
    url_input = None

    if input_type == "Text":
        text_input = st.text_area("Enter Text")

    elif input_type == "File Upload":
        file_input = st.file_uploader(
            "Upload file",
            type=["mp3", "wav", "mp4", "csv", "xlsx"]
        )

    elif input_type == "URL":
        url_input = st.text_input("Enter URL")

    if st.button("🚀 Analyze"):

        with st.spinner("Processing..."):

            try:
                files = {}
                data = {}

                if text_input:
                    data["text"] = text_input

                elif file_input:
                    files["file"] = (file_input.name, file_input, file_input.type)

                elif url_input:
                    data["url"] = url_input

                response = requests.post(API_ANALYZE, data=data, files=files)
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                    st.stop()

                # ======================================================
                # DATASET MODE
                # ======================================================

                if result.get("mode") == "dataset_evaluation":

                    st.success("Dataset Evaluation Complete")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("Accuracy", result["accuracy"])
                    col2.metric("Precision", result["precision"])
                    col3.metric("Recall", result["recall"])
                    col4.metric("F1 Score", result["f1_score"])

                    st.subheader("📊 Confusion Matrix")
                    st.image(result["heatmap_file"])

                # ======================================================
                # NORMAL OUTPUT
                # ======================================================

                else:

                    st.markdown("### 📊 Moderation Summary")

                # -------------------------------
                # COMPACT METRICS (INLINE STYLE)
                # -------------------------------

                    col1, col2, col3 = st.columns(3)

                    col1.markdown(f"**Label:** `{result['label']}`")
                    col2.markdown(f"**Severity:** `{result['severity']}/5`")
                    col3.markdown(f"**Confidence:** `{result['confidence']}`")

                # -------------------------------
                # SMALL PROGRESS BAR
                # -------------------------------

                    st.progress(min(result["severity"] / 5, 1.0))

                # -------------------------------
                # COMPACT WORD DISPLAY
                # -------------------------------

                    offensive = result["matched_offensive_words"]
                    explicit = result["matched_explicit_words"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.caption("Offensive Words")
                        st.write(", ".join(offensive) if offensive else "—")

                    with col2:
                        st.caption("Explicit Words")
                        st.write(", ".join(explicit) if explicit else "—")

                    # -------------------------------
                    # MINI WORD GRAPH (OPTIONAL)
                    # -------------------------------

                    all_words = offensive + explicit

                    if all_words:

                        from collections import Counter
                        import matplotlib.pyplot as plt

                        word_counts = Counter(all_words)

                        fig, ax = plt.subplots(figsize=(4,2))
                        ax.bar(word_counts.keys(), word_counts.values())
                        ax.set_xticklabels(word_counts.keys(), rotation=30)
                        ax.set_title("Word Frequency", fontsize=8)

                        st.pyplot(fig)

                    # -------------------------------
                    # PREDICTED WORDS (MINIMAL)
                    # -------------------------------

                    if result["predicted_words"]:
                        st.caption("Predicted Words")
                        st.write(result["predicted_words"])

                    # -------------------------------
                    # COLLAPSIBLE FULL RESPONSE
                    # -------------------------------

                    with st.expander("Full Response"):                
                        st.json(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
# ==========================================================
# TAB 2: WORD MANAGEMENT
# ==========================================================

with tab2:

    col1, col2 = st.columns(2)

    # -------- ADD WORD --------
    with col1:
        st.subheader("➕ Add Word")

        new_word = st.text_input("Word")
        word_type = st.selectbox("Type", ["offensive", "explicit"])

        if st.button("Add Word"):

            if new_word.strip():

                res = requests.post(API_ADD, data={
                    "word": new_word,
                    "category": word_type
                }).json()

                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success(res.get("message", "Word added"))

            else:
                st.warning("Enter valid word")

    # -------- DELETE WORD --------
    with col2:
        st.subheader("❌ Delete Word")

        delete_word = st.text_input("Word to delete")

        if st.button("Delete Word"):

            if delete_word.strip():

                res = requests.post(API_DELETE, data={
                    "word": delete_word
                }).json()

                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success(res.get("message", "Deleted"))

            else:
                st.warning("Enter valid word")