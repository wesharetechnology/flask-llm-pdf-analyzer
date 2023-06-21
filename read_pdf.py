import re
import PyPDF2

def extract_sentences(file_path):
    # Open the PDF file in binary mode
    pdf_file = open(file_path, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Loop over each page in the file
    all_sentences = []
    for page_num in range(pdf_reader.getNumPages()):
        # Extract the text from the page
        page = pdf_reader.getPage(page_num)
        text = page.extractText()

        # Split the text into sentences using regex
        sentences = re.split('[.!?]', text)

        # Add the sentences to the list of all sentences
        all_sentences.extend(sentences)

    # Close the PDF file
    pdf_file.close()
    return all_sentences
    # Print all the extracted sentences