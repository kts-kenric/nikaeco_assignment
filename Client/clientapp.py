from flask import Flask, request, jsonify, current_app, Response, make_response, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from createEmeddings import *
from model import *
from langchain.prompts import PromptTemplate
from helper import *
from langchain.schema import prompt
from langchain.embeddings import HuggingFaceBgeEmbeddings


ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = 'pdf'




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_uploads_folder(folder):
    for file in os.scandir(app.config['UPLOAD_FOLDER']):
        if file.name.endswith(".pdf"):
            os.unlink(file.path)


def init_model():
    llm = TogetherLLM(
    model= "togethercomputer/llama-2-7b-chat",
    temperature = 0.1,
    max_tokens = 1024)
    return llm

def init_prompt_template():
    sys_prompt = """You are a helpful, respectful and honest assistant who loves the climate and summarizing enviromental related pdf. Always answer as helpfully as possible using the context text provided. Your answers should only answer the question once and not have any text after the answer is done.

    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. """

    instruction = """CONTEXT:/n/n {context}/n

    Question: {question}"""

    prompt_template = get_prompt(instruction, sys_prompt)

    llama_prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": llama_prompt}
    return chain_type_kwargs

def init_db():
    model_name = "BAAI/bge-base-en"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cuda'},
        encode_kwargs=encode_kwargs
)

    # Embed and store the texts
    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'

    ## Here is the nmew embeddings being used
    embedding = model_norm

    vectordb = Chroma(persist_directory = persist_directory, embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k" : 3 })
    return retriever

def init_qa_chain(llm,retriever,chain_type_kwargs):
    # create the chain to answer questions
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        chain_type_kwargs=chain_type_kwargs,
                                        return_source_documents=True)
    return qa_chain



#@TODO SETUP CHAIN
#@TODO SETUP WEBSITE

# while True:
#     user_input = input("Hi i am stupid bot please type ur question: ")
#     print(user_input)
#     llm_response = qa_chain(user_input)
#     print(process_llm_response(llm_response))


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Pong!'})

@app.route('/input', methods=['POST'])
def process_input():
    if 'user_input' not in request.form:
        return jsonify({'error': 'No user_input provided'}), 400
    user_input = request.form['user_input']
    llm_response = qa_chain(user_input)
    output = process_llm_response(llm_response)
    print(output)
    print(type(output))
    return (output, 200)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})

    files = request.files.getlist('file')

    if len(files) == 0:
        return jsonify({'message': 'No files uploaded'})

    clear_uploads_folder(app.config['UPLOAD_FOLDER'])  # Clear uploads folder before saving new files

    uploaded_files = []
    for file in files:
        if file.filename == '':
            return jsonify({'message': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(filename)
        else:
            return jsonify({'message': 'Invalid file format'})
    createEmbeddings()
    print("Embeddings created")
    with app.app_context():
        print("app is re-init")
        retriever = init_db()
        llm = init_model()
        chain_type_kwargs = init_prompt_template()
        qa_chain = init_qa_chain(llm,retriever,chain_type_kwargs)
    return jsonify({'message': 'Files uploaded successfully', 'uploaded_files': uploaded_files})


if __name__ == '__main__':
    with app.app_context():
        print("app is init")
        retriever = init_db()
        llm = init_model()
        chain_type_kwargs = init_prompt_template()
        qa_chain = init_qa_chain(llm,retriever,chain_type_kwargs)
    print("app is running")
    app.run(host='127.0.0.1', port=4000,threaded=False)