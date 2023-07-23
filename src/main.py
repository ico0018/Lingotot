from fastapi import FastAPI, Depends, UploadFile, File
from typing import Optional
from usersession import UserSession

app = FastAPI()

def get_user_session():
    with UserSession() as openai_instance:
        yield openai_instance

@app.post("/string_length")
async def get_string_length(string: str):
    return {"length": len(string)}

@app.post("/send_message_gpt3/")
async def send_message_gpt3(
    user_prompt: str, 
    assistant_prompt: Optional[str] = None, 
    system_prompt: Optional[str] = "You are a helpful assistant.",
    openai_instance = Depends(get_user_session)
):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    if assistant_prompt:
        messages.append({"role": "assistant", "content": assistant_prompt})

    response = openai_instance.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return response.choices[0].message['content']

@app.post("/send_voice_message/")
async def send_voice_message(
    audio_file: UploadFile = File(...), 
    system_prompt: Optional[str] = "You are a helpful assistant.",
    openai_instance = Depends(get_user_session)
):
    # Transcribe the audio file with Whisper
    whisper_response = openai_instance.Whisper.read(file=audio_file.file.read())
    transcribed_text = whisper_response['transcript']

    # Send the transcribed text to GPT-3
    gpt_response = openai_instance.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcribed_text}
        ]
    )
    return gpt_response.choices[0].message['content']