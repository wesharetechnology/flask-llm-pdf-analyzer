import os
from pathlib import Path
from dotenv import load_dotenv

# 向量数据库
from langchain.vectorstores import Chroma

# 文档加载器
from langchain.document_loaders import PyPDFLoader

# 文本转换为向量的嵌入引擎
from langchain.embeddings.openai import OpenAIEmbeddings

# 文本拆分
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import Azure OpenAI
from langchain.chains import RetrievalQA

# Import Azure OpenAI
# from langchain.llms import AzureOpenAI
import openai
from langchain.chat_models import AzureChatOpenAI

print(Path.cwd())

# 加载环境变量
load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"  # API 版本，未来可能会变
openai.api_base = "https://hkust.azure-api.net"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# 本地PDF文件夹位置
pdf_base_dir = "./data/uCap"
# 本地数据库位置
db_dir = "./db/chroma"


azure_embeddeing = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_base="https://hkust.azure-api.net",
    openai_api_type="azure",
)

#  创建Azure OpenAI的实例
llm_chat = AzureChatOpenAI(
    openai_api_version=openai.api_version,
    deployment_name="gpt-35-turbo",
    openai_api_key=openai.api_key,
    openai_api_type="azure",
    openai_api_base="https://hkust.azure-api.net",
    temperature=0,
)
# 向量数据库
vectordb = Chroma(embedding_function=azure_embeddeing, persist_directory=db_dir)

# 构建检索方式
retriever = vectordb.as_retriever()


def load_pdfs(file_folder_path) -> list:
    """
    将本地pdf加载到loader中
    """
    pdf_list = []
    for item in os.listdir(file_folder_path):
        loader = PyPDFLoader(file_path=os.path.join(file_folder_path, item))
        pdf_list.append(loader.load())
    return pdf_list


def split_pdfs(file_list: list, chunk_size=1000, chunk_overlap=400) -> list:
    """
    拆分pdf为文本段
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    content_list = []
    for pdf in file_list:
        content_list.append(text_splitter.split_documents(pdf))
        print("拆分文档数：", len(docs))
    return content_list


def get_enbeddings(
    embeddings,
    content_list,
    persist_directory,
):
    """
    将文本结果进行词嵌入获取向量
    """
    # 向量化
    # 会对 OpenAI 进行 API 调用
    vectordb = Chroma(
        embedding_function=embeddings, persist_directory=persist_directory
    )
    for content in content_list:
        vectordb.add_documents(content)
    # 持久化
    vectordb.persist()
    # 准备嵌入引擎


def search_from_chroma(query):
    """
    从chroma数据库中寻找本地相近文本
    """
    db = Chroma(embedding_function=azure_embeddeing, persist_directory=db_dir)
    related_doc = db.similarity_search(query)
    print(related_doc[0])


def query_LLM(llm):
    """
    使用语言模型进行回答
    """
    # 通过langchain构建一个问答链
    chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )

    # # 循环接收用户输入并进行问答

    while True:
        user_input = input("请输入问题进行问答：")
        result = chain({"query": user_input})
        print(result["result"])


if __name__ == "__main__":
    ##### 构建本地chroma数据库
    # local_files = load_pdfs(pdf_base_dir)
    # docs = split_pdfs(local_files)
    # # 统计总共的文本量
    # print("提取文本量：", len(docs))
    # get_enbeddings(
    #     embeddings=azure_embeddeing, persist_directory=db_dir, content_list=docs
    # )

    ###### 测试本地数据集寻找与query相似的文本段
    # while True:
    #     q = input()
    #     search_from_chroma(q)

    ###### 使用语言模型结合chroma进行问答
    query_LLM(llm_chat)
