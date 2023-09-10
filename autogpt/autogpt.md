# AutoGPT的Gradio版本

基于AutoGPT，加上Gradio的控制，在prompt中指定了输出文件名字如<code>output.txt</code>，Gradio调用完agent之后读取output.txt的内容作为输出，详细请看[autogpt_chat.py](autogpt_chat.py)