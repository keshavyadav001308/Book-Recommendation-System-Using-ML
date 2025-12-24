import streamlit as st
import pickle
import os

# -----------------------------
# Load Pickle Files
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

books_path = os.path.join(BASE_DIR, "model", "books.pkl")
cosine_path = os.path.join(BASE_DIR, "model", "cosine_sim.pkl")

df = pickle.load(open(books_path, "rb"))
cosine_sim = pickle.load(open(cosine_path, "rb"))

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend_books(book_title, top_n=5):

    book_title = book_title.strip()

    matches = df[df['title'].str.strip().str.casefold() == book_title.casefold()]
    if matches.empty:
        return []

    index = matches.index[0]

    similarity_scores = list(enumerate(cosine_sim[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_matches = similarity_scores[1: top_n + 1]

    results = []
    for i, score in top_matches:
        results.append({
            "title": df.iloc[i]['title'],
            "author": df.iloc[i]['authors'],
            "thumbnail": df.iloc[i]['thumbnail']
        })

    return results

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Book Recommendation System", layout="wide")

st.title("📚 Book Recommendation System")
st.write("Get similar book recommendations based on content similarity.")

# Dropdown to select book
selected_book = st.selectbox(
    "Select a book",
    df['title'].values
)

# Button
if st.button("Recommend"):
    recommendations = recommend_books(selected_book)

    if not recommendations:
        st.error("Book not found!")
    else:
        st.subheader("🔍 Recommended Books")

        cols = st.columns(5)

        for col, book in zip(cols, recommendations):
            with col:
                if book["thumbnail"]:
                    st.image(book["thumbnail"], use_container_width=True)
                else:
                    st.write("📕 No Image")

                st.markdown(f"**{book['title']}**")
                st.caption(f"✍️ {book['author']}")
