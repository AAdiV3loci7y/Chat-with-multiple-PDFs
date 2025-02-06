# Chat with Multiple PDFs 📄🤖

This repository enables users to upload multiple PDF files and interact with them using a chatbot interface. It utilizes **LangChain** and **Pinecone** for embedding-based document search and retrieval, combined with an **LLM (Large Language Model)** for generating responses.

## Features 🚀
- Upload multiple PDF files.
- Process documents into text chunks.
- Perform **semantic search** using **Pinecone**.
- Retrieve relevant document passages for user queries.
- Generate responses with an **LLM**.
- Simple and user-friendly interface.

## How It Works 🔍
![How It Works](https://i.ibb.co/q3qR3PZs/Remodeled-pdf.jpg)
1. **Upload PDFs** 📂
   - Users can upload multiple PDF documents via the UI.

2. **Chunking and Embedding** 🔢
   - The PDFs are split into smaller text chunks.
   - Each chunk is converted into an embedding (vector representation).

3. **Semantic Search & Retrieval** 🧠
   - When a query is entered, it is also converted into an embedding.
   - A similarity search is performed in **Pinecone**, retrieving the most relevant document chunks.

4. **Answer Generation** 📝
   - The retrieved text is passed to an LLM to generate a final response.

### User Interface
![How It Works](https://i.ibb.co/fVm7rCLj/user-face-llm-pdf.png)

## Installation 🏗️
To run this project on your local machine:

1. Clone the repository:
   ```sh
   git clone <your-repository-link-here>
   cd Chat-with-multiple-PDFs
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your **Hugging Face API Key** (or optionally OpenAI API Key) in the `.env` file:
   ```sh
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
   # Uncomment below if you want to use OpenAI API instead
   # OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Adjustments and Fixes 🛠️
This project was inspired by a tutorial by [Alejandro AO]([https://www.youtube.com/@alejandro-ao](https://www.youtube.com/@alejandro_ao)). Adjustments have been made with the help of **ChatGPT-4.0** to fix bugs, errors and improve functionality. 

## Acknowledgments 🙌
I would like to thank **[Alejandro AO - Software & AI](https://www.youtube.com/@alejandro-ao)** for his informative tutorial. His video [here](https://www.youtube.com/watch?v=dXxQ0LR-3Hg) provided valuable insights that helped in building and improving this project.

## License 📜
This project is open-source under the MIT License.

---

Enjoy chatting with your PDFs! 🎉

