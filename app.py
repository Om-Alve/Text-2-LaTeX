import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor
from dotenv import load_dotenv

import gradio as gr

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
class Output(BaseModel):
    latex: str

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)


def get_LaTeX(query):
    prompt = f"""
    You are a tool which takes in natural language descriptions and give out LaTeX according to the instructions in the input
    Output LaTeX for the following:
    {query}
    """
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_model=Output,
    )
    return resp.latex,"$$\\begin{align*}" + resp.latex + "\\end{align*}$$"

css = """
    #submit-btn {
        background: #8957E5;
    }
"""

with gr.Blocks(theme=gr.themes.Default(primary_hue="purple"),css=css) as demo:
    gr.HTML("<h1><center>Text to LaTeX<center><h1>")
    gr.HTML("<h3><center>Just type a query in natural language and get back LaTeX, you can verify it by looking at the rendered LaTeX!</center></h3>")
    with gr.Row():
        with gr.Column():
            input = gr.Textbox(label="Input Text")
            submit_btn = gr.Button(value='Submit',elem_id='submit-btn')
        with gr.Column():
            output = gr.Text(label='LaTeX',interactive=False)
            rendered_latex = gr.Markdown(label="Rendered LaTeX")
        
    gr.on(
        triggers=[input.submit, submit_btn.click],
        inputs=input,
        fn=get_LaTeX,
        outputs=[output,rendered_latex]
    )
if __name__ == "__main__":
    demo.launch(share=True)




