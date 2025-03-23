import tempfile
import edge_tts
import gradio as gr
import asyncio

language_dict = {
    "Amharic": {
        "Ameha": "am-ET-AmehaNeural",
        "Mekdes": "am-ET-MekdesNeural"
    }
}

async def text_to_speech_edge(text, speaker):
    voice = language_dict["Amharic"][speaker]
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        # Create temp file with increased timeout
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
            await asyncio.wait_for(communicate.save(tmp_path), timeout=30)
            
        return tmp_path
        
    except asyncio.TimeoutError:
        error_msg = "ስህተት: ጊዜ አልቋል። እባክዎ እንደገና ይሞክሩ። (Timeout)"
        raise gr.Error(error_msg)
    except Exception as e:
        error_msg = f"ስህተት: ድምፅ መፍጠር አልተቻለም።\nError: {str(e)}"
        raise gr.Error(error_msg)

with gr.Blocks(title="Amharic TTS") as demo:
    gr.HTML("<center><h1>Amharic Text-to-Speech</h1></center>")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(lines=5, label="የአማርኛ ጽሑፍ", 
                                  placeholder="ድምፅ ለመፍጠር ጽሑፍ ያስገቡ...")
            speaker = gr.Dropdown(
                choices=["Ameha", "Mekdes"],
                value="Ameha",
                label="አርቲስት"
            )
            run_btn = gr.Button(value="ድምፅ ፍጠር", variant="primary")

        with gr.Column():
            output_audio = gr.Audio(type="filepath", label="የድምፅ ውጤት")

    run_btn.click(
        text_to_speech_edge,
        inputs=[input_text, speaker],
        outputs=output_audio
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
