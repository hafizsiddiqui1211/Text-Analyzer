import streamlit as st
import re
from collections import Counter
import base64
import streamlit.components.v1 as components


def speak_with_browser(text):
    # Escape JS-breaking characters
    escaped_text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{escaped_text}");
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code)


def download_button(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Modified Text</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.button("Download")


def main():
    # 🧾 Page config
    st.set_page_config(page_title="Text Analyzer", page_icon="📜", layout="centered")

    st.title("📊 Text Analyzer by Hafiz Siddiqui")
    st.info("🔍 Type your paragraph below to analyze, modify, and explore features.")

    paragraph = st.text_area("📝 Write your paragraph:", "", height=150)

    if st.button("Analyze"):
        if paragraph.strip() == "":
            st.warning("⚠️ Pehle koi paragraph likho phir Analyze karo.")
            return

        st.markdown("---")
        st.subheader("💯 Analysis Result")

        words = paragraph.split()
        word_count = len(words)
        char_count = len(paragraph)

        col1, col2 = st.columns(2)
        col1.metric("🆎 Total Words", word_count)
        col2.metric("✍️ Total Characters", char_count)

        with st.expander("📌 Word Frequency Count"):
            word_freq = Counter(words)
            for word, freq in word_freq.items():
                st.write(f"🔁 `{word}`: {freq} times")

        with st.expander("🔁 Search and Replace Feature"):
            search_word = st.text_input("🔍 Word to search:")
            replace_word = st.text_input("✏️ Replace with (optional):")

            modified_paragraph = paragraph

            if search_word:
                st.markdown("📌 **Highlighted Paragraph:**")
                highlighted = re.sub(
                    rf"\b({re.escape(search_word)})\b",
                    r"**\1**",
                    modified_paragraph,
                    flags=re.IGNORECASE,
                )
                st.markdown(highlighted)

            if search_word and replace_word:
                modified_paragraph = re.sub(
                    rf"\b{re.escape(search_word)}\b",
                    replace_word,
                    modified_paragraph,
                    flags=re.IGNORECASE,
                )
                st.success("✅ Word replaced successfully!")

            if modified_paragraph != paragraph:
                st.text_area("📝 Modified Paragraph:", modified_paragraph, height=150)
                download_button(modified_paragraph, "modified_text.txt")

        with st.expander("🔠 Case Transformations"):
            st.text_area("🔡 Lowercase:", modified_paragraph.lower(), height=100)
            st.text_area("🔠 UPPERCASE:", modified_paragraph.upper(), height=100)

        with st.expander("📢 Read Text Aloud (Browser-Based)"):
            if st.button("🔊 Speak"):
                speak_with_browser(modified_paragraph)


if __name__ == "__main__":
    main()
