from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GenerateRequest(BaseModel):
    topic: str
    length: int
    temperature: float = 0.7
    genre: str = None
    narrative_perspective: str = None
    character_name: str = None
    character_description: str = None
    setting_description: str = None


class CompleteRequest(BaseModel):
    partial_story: str
    length: int
    temperature: float = 0.7
    genre: str = None
    narrative_perspective: str = None
    character_name: str = None
    character_description: str = None
    setting_description: str = None


@app.post("/generate")
def generate_story(request: GenerateRequest):
    response = generate(
        topic=request.topic,
        length=request.length,
        temperature=request.temperature,
        genre=request.genre,
        narrative_perspective=request.narrative_perspective,
        character_name=request.character_name,
        character_description=request.character_description,
        setting_description=request.setting_description
    )
    return {"story": response}


@app.post("/complete")
def complete_story(request: CompleteRequest):
    response = complete(
        partial_story=request.partial_story,
        length=request.length,
        temperature=request.temperature,
        genre=request.genre,
        narrative_perspective=request.narrative_perspective,
        character_name=request.character_name,
        character_description=request.character_description,
        setting_description=request.setting_description
    )
    return {"completed_story": response}
