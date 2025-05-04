import google.generativeai as genai
import PyPDF2

class CVModel:
    def __init__(self, api_key, model_name):
        """
        Initializes the CVModel with the given API key and model name.
        
        Args:
            api_key (str): The API key for authentication.
            model_name (str): The name of the generative model to use.
        """
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def summarize_cv(self, pdf_path, format_template):
        """Reads a CV from a PDF and summarizes it using the Gemini API."""
        cv_text = self.read_pdf(pdf_path)
        if "Error:" in cv_text:
            return cv_text  # Return the error message

        prompt = f"""Summarize the following CV according to this format:

        {format_template}

        CV:
        {cv_text}
        """
        response = self.model.generate_content(prompt)
        return response.text
    
    def read_pdf(self, pdf_path):
        """Reads the text content from a PDF file."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or "" #Handle potential empty pages
        except FileNotFoundError:
            return f"Error: File not found at {pdf_path}"
        except Exception as e:
            return f"An error occurred: {e}"
        return text
