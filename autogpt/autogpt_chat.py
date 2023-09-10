import gradio as gr
import os
import openai

from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

# 构造 AutoGPT 的工具集
search = SerpAPIWrapper()
tools = [
    Tool(
        name="search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    WriteFileTool(),
    ReadFileTool(),
]

from langchain.embeddings import OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings()
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

# OpenAI Embedding 向量维数
embedding_size = 1536
# 使用 Faiss 的 IndexFlatL2 索引
index = faiss.IndexFlatL2(embedding_size)
# 实例化 Faiss 向量数据库
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

from langchain_experimental.autonomous_agents import AutoGPT
from langchain.chat_models import ChatOpenAI

agent = AutoGPT.from_llm_and_tools(
    ai_name="Jarvis",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(), # 实例化 Faiss 的 VectorStoreRetriever
)

agent.chain.verbose = True

def chat_fn(message, history):
    agent.run([message,"结果存在名为output.txt的文件"])
    with open("output.txt") as f:
        return f.readline()

def launch_gradio():
    with gr.Blocks() as demo:
        chatbot_component = gr.Chatbot(height=600, render=False)
        chat_interface = gr.ChatInterface(
            fn=chat_fn,
            title="autogpt chating",
            # retry_btn=None,
            # undo_btn=None,
            chatbot= chatbot_component,
        )

    demo.launch(share=False, server_name="0.0.0.0")

if __name__ == "__main__":
    # 启动 Gradio 服务
    launch_gradio()