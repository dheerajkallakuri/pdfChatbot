# PDF Chatbot using Retrieval Augmented Generation (RAG)

This project implements a PDF chatbot powered by **Retrieval Augmented Generation (RAG)**. It allows users to upload any PDF document, analyze its contents, and answer the questions related to the uploaded file. The chatbot responds based on the PDF's content and can refuse to reply if the requested information is not present in the document.

<img width="1116" alt="app" src="https://github.com/user-attachments/assets/81cab820-73bb-4d86-95e2-02884bdabd8d">



## Key Features
- **PDF Upload & Analysis**: Upload any PDF file and have it automatically analyzed for content extraction.
- **Interactive Chatbot**: Ask questions related to the uploaded PDF and receive contextual answers.
- **Out-of-Scope Responses**: If the required information is missing from the PDF, the chatbot can provide a relevant response.

## RAG Architecture Overview
- **Document Chunking**: The PDF is split into smaller chunks to manage the document efficiently during retrieval.
- **Embeddings**: Each chunk is embedded into a high-dimensional space to represent the content numerically.
- **Vector Store**: The embedded chunks are stored in a vector database, enabling fast similarity searches based on the user’s query.
- **Retriever-LLM**: The retriever finds the most relevant chunks from the vector store, which are passed to a language model (LLM) to generate responses.
- **Augmented Responses**: The LLM synthesizes answers by using both the retrieved context from the PDF and its own pre-trained knowledge.

![rag_arch](https://github.com/user-attachments/assets/f5597787-39d9-45c8-a703-c060b4ba505c)


## Project Structure

### 1. `app.py` - The User Interface
This file handles the UI components for the project, built with two primary sections:
- **Left Panel**: 
  - *Upload Button*: Allows the user to upload a PDF file.
  - *Analyze Button*: Analyzes the uploaded PDF and prepares it for question answering.
- **Right Panel**:
  - *Chat Area*: Displays the chat history between the user and the chatbot.
  - *User Input Area*: A textbox for the user to input questions with a send button to submit the queries.
 
<img width="814" alt="gui" src="https://github.com/user-attachments/assets/396a7d51-9028-4191-8b15-6adc23af6c7f">


### 2. `ragModel.py` - The Core Logic
This file handles the following:
- **PDF Analysis**: Processes the uploaded PDF, chunks the document, and embeds each chunk.
- **Vector Database & Retriever**: The chunks are stored in a vector database for efficient retrieval.
- **Query Processing**: When the user asks a question, it is embedded, and relevant chunks are retrieved from the vector store.
- **LLM Integration**: The retrieved information is passed to the language model for generating responses.

### 3. `grammarCheck.py` - Grammar and Spelling Check
This file handles grammar and spelling correction of user inputs:
- **User Input Correction**: It checks for spelling and grammar errors in the user's query and replaces the corrected version in the chat area.
- **Punctuation Handling**: Note that this project version does not handle punctuation.
<table>
  <tr>
    <td><img width="503" alt="gchck1" src="https://github.com/user-attachments/assets/f0f6b292-cc5b-489e-99b9-09613dbc055d"></td>
    <td><img width="499" alt="gchck2" src="https://github.com/user-attachments/assets/d49942ec-19eb-4a4e-a68e-824a8dea3e34"></td>
  </tr>
</table>

## How to Run the Project

1. **Install Requirements**: Install all required libraries using the `requirements.txt` file by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/dheerajkallakuri/pdfChatbot.git
   ```

3. **Run the Application**:
   Navigate to the project directory and run:
   ```bash
   python app.py
   ```

## Conclusion
This PDF chatbot leverages RAG to create an interactive and intelligent interface for users to engage with any PDF content effectively. It enhances the document experience by providing accurate and context-driven responses.
