import streamlit as st
from fewshots import FewShotPosts

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def main():
    st.title("LinkedIn Echo")
    # three columns for dropdown
    col1 , col2 , col3 = st.columns(3)
    fs = FewShotPosts()
    tags = fs.get_tags()

    # dropdown for topic
    with col1:
        selected_tag = st.selectbox("Title",options=tags)
    # dropdown for length
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    # dropdown for language
    with col3:
        selected_language = st.selectbox("Language", options=language_options)


   # generate button
   if st.button("Generate"):
       post = generate_post(selected_length,selected_language,selected_tag)
       st.write(post)


if __name__ == "__main__":
    main()