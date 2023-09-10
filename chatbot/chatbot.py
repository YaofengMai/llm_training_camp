import gradio as gr
import random
import time

from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import os
import openai

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
embedding = OpenAIEmbeddings()


def initialize_sales_bot():
    real_estate_db = FAISS.load_local("real_estates_sale", embedding)
    
    global REAL_ESTATES_BOT    
    REAL_ESTATES_BOT = RetrievalQA.from_chain_type(llm,
                                           retriever=real_estate_db.as_retriever(search_type="similarity_score_threshold",
                                                                     search_kwargs={"score_threshold": 0.8}))
    # 返回向量数据库的检索结果
    REAL_ESTATES_BOT.return_source_documents = True

    home_decoration_db = FAISS.load_local("home_decoration", embedding)
    global HOME_DECORATION_BOT
    HOME_DECORATION_BOT = RetrievalQA.from_chain_type(llm,
                                           retriever=home_decoration_db.as_retriever(search_type="similarity_score_threshold",
                                                                     search_kwargs={"score_threshold": 0.8}))
    # 返回向量数据库的检索结果
    HOME_DECORATION_BOT.return_source_documents = True
    
    education_db = FAISS.load_local("education", embedding)
    global EDUCATION_BOT
    EDUCATION_BOT = RetrievalQA.from_chain_type(llm,
                                           retriever=education_db.as_retriever(search_type="similarity_score_threshold",
                                                                     search_kwargs={"score_threshold": 0.8}))
    EDUCATION_BOT.return_source_documents = True
    
    global last_bot
    last_bot = -1

def chat_fn(message, history, library):
    global last_bot
    print(f"library to use:{library}")
    print(f"global last_bot:{last_bot}")
    print(f"[message]{message}")
    print(f"[history]{history}")
    # TODO: 从命令行参数中获取
    enable_chat = True

    if library == 0:
        bot = REAL_ESTATES_BOT
    elif library == 1:
        bot = HOME_DECORATION_BOT
    elif library == 2:
        bot = EDUCATION_BOT
        
    if library != last_bot:
        history.clear()
        last_bot = library
    ans = bot({"query": message})
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return "这个问题我要问问领导"
    

def launch_gradio():
    with gr.Blocks() as demo:
        library = gr.Dropdown(choices=["房产","家装", "教育"], type="index", value = "房产", label="行业")
        chatbot_component = gr.Chatbot(height=600, render=False)
        chat_interface = gr.ChatInterface(
            fn=chat_fn,
            title="销售",
            # retry_btn=None,
            # undo_btn=None,
            chatbot= chatbot_component,
            additional_inputs= [ library]
        )
        library.input(fn=reset, inputs=library, outputs=[chatbot_component, chat_interface.chatbot_state])

    demo.launch(share=False, server_name="0.0.0.0")

def reset(z):
    return [], []

if __name__ == "__main__":
    # 初始化房产销售机器人
    initialize_sales_bot()
    # 启动 Gradio 服务
    launch_gradio()
