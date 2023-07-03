"""
This read the PDF file obtained from the POST method and split it into sentences
"""
import re
import PyPDF2

def extract_sentences(file_path):
    """
    input: the PDF in current directory
    output: a list of sentences
    """
    all_sentences = []
    # Open the PDF file in binary mode
    with open(file_path, 'rb') as pdf_file:

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)

        # Loop over each page in the file
        for page_num in range(0, pdf_reader.getNumPages()-2):
            # Extract the text from the page
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            # Split the text into sentences using regex
            sentences = re.split('[.!?]', text)

            # Add the sentences to the list of all sentences
            all_sentences.extend(sentences)

    # Close the PDF file
    return all_sentences
