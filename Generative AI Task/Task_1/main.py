import fitz

from fpdf import FPDF
from openai import OpenAI

client = OpenAI()

SUMMARIZER_MODEL = "gpt-4o-mini-2024-07-18"
MAX_TOKENS = 400   # Approximate number of tokens to fit into a page

def summarize_text(text):
    """
    This function summarizes the input text using GPT.
    """
    response = client.chat.completions.create(
        model=SUMMARIZER_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text chunks provided from books."},
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ],
        temperature=0.7,
        max_tokens=MAX_TOKENS
    )
    summary = response.choices[0].message.content
    return summary

def replace_unicode_characters(text):
    unicode_alternatives = {
        "–": "-", "—": "-", "―": "-", "‗": "=", "‘": "'", "’": "'", "‚": ",", "‛": "'",
        "“": '"', "”": '"', "•": "->", "′": "'", "″": '"', "‹": "<", "›": ">"
    }
    for key, value in unicode_alternatives.items():
        if key in text:
            key = key.replace(key, value)
    return text

class PDF(FPDF):
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(summary_filepath, summaries):
    """
    This function creates a PDF file for the text chunks provided.
    """
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.chapter_title("Summary of Crime and Punishment")
    for chapter_num, summary in enumerate(summaries, start=1):
        summary = replace_unicode_characters(summary)
        try:
            summary = summary.encode("latin-1", "replace").decode("latin-1")
        except UnicodeEncodeError as e:
            print(f"Encoding error in chapter {chapter_num}: {e}")
        pdf.chapter_title(f"Chapter {chapter_num}")
        pdf.chapter_body(summary)
    pdf.output(summary_filepath)
    print("PDF summary created successfully.")

def get_book_text(filepath):
    """
    This functions extracts all text from the book
    """
    book_text = ""
    with fitz.open(filepath) as pdf:
        for page in pdf:
            book_text += page.get_text()
    return book_text

def get_book_chunks(book_text, number_of_pages):
    """
    This function breaks down the book into chunks
    """
    chunk_size = int(len(book_text) / number_of_pages)

    chunks = []
    start_index = end_index = 0
    for i in range(number_of_pages):
        start_index = end_index
        end_index = i * chunk_size
        # Ensure that each chunk ends at the end of a sentence rather than in the middle of a sentence or word.
        if book_text[end_index] != '.':
            remaining_chunk = book_text[end_index:]
            next_dot = remaining_chunk.find('.')
            end_index += next_dot
        chunk = book_text[start_index:end_index]
        if len(chunk) > 100:
            chunks.append(chunk)

    if len(chunks) == 20:
        chunks[19] += book_text[end_index:]
    elif len(chunks) == 19:
        chunks.append(book_text[end_index:])
    return chunks

if __name__ == "__main__":
    filepath = "C:/Users/Dell/Documents/RhodiumTech/MedAI/Code/My Code/Generative AI Task/crime_and_punishment.pdf"
    book_text = get_book_text(filepath)
    
    number_of_pages = 20
    chunks = get_book_chunks(book_text, number_of_pages)
    
    summarized_chunks = []
    for chunk in chunks:
        summary = summarize_text(chunk)
        summarized_chunks.append(summary)

    summary_filepath = "C:/Users/Dell/Documents/RhodiumTech/MedAI/Code/My Code/Generative AI Task/Crime_and_Punishment_Summary.pdf"
    create_pdf(summary_filepath, summarized_chunks)
