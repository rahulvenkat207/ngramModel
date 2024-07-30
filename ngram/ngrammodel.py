import random
import streamlit as st

class NGRAM:
    def __init__(self, n):
        self.n = n
        self.ngram_prob = {}

    def load_data(self, file):
        data = file.read().decode("utf-8")
        return data

    def preprocess_text(self, data):
        text = data.lower()
        text = text.split()
        return text

    def preprocess_data(self, data):
        preprocessed_text = self.preprocess_text(data)
        return preprocessed_text

    def build_ngrams(self, words):
        ngrams = []

        for i in range(len(words) - self.n + 1):
            ngrams.append(tuple(words[i:i + self.n]))
        return ngrams

    def calculate_probabilities(self, ngrams):
        ngram_count = {}

        for ngram in ngrams:
            if ngram in ngram_count:
                ngram_count[ngram] += 1
            else:
                ngram_count[ngram] = 1

        total = sum(ngram_count.values())

        for ngram, count in ngram_count.items():
            self.ngram_prob[ngram] = count / total

        return self.ngram_prob

    def generate_text(self, length=100):
        generated_text = list(random.choice(list(self.ngram_prob.keys())))

        for _ in range(length - self.n):
            context = tuple(generated_text[-(self.n - 1):])
            possible_next_word = [ngram[-1] for ngram in self.ngram_prob if ngram[:-1] == context]
            next_word = random.choices(possible_next_word, weights=[self.ngram_prob[ngram] for ngram in self.ngram_prob if ngram[:-1] == context])[0]
            generated_text.append(next_word)
        return ' '.join(generated_text)

st.title("NGRAM Text Generator")
st.write("Upload a text file to generate text using an NGRAM model.")

uploaded_file = st.file_uploader("Choose a file", type=["txt"])
n = st.number_input("Enter the value of n for n-gram (1-10):", min_value=1, max_value=10, value=3)
length = st.number_input("Enter the length of the generated text:", min_value=10, max_value=1000, value=100)

if uploaded_file is not None:
    model = NGRAM(n)
    data = model.load_data(uploaded_file)
    
    preprocessed_data = model.preprocess_data(data)
    b_ngrams = model.build_ngrams(preprocessed_data)
    model.calculate_probabilities(b_ngrams)
    
    result = model.generate_text(length)
    paragraphs = result.split('. ')
    formatted_text = '\n\n'.join(paragraphs)
    
    st.write("Generated Text:")
    st.markdown(formatted_text)
