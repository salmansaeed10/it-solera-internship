import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from dotenv import  load_dotenv
 
dotenv_path = '.env'
load_dotenv(dotenv_path)
GROQ_API = os.getenv('GROQ_API')
 
def chat_model(temperature):
    return ChatGroq(temperature=temperature,
                    model_name="Llama3-70b-8192",
                    api_key=GROQ_API,
                    max_tokens=1000,
                    model_kwargs={
                        "top_p": 1,
                        "frequency_penalty": 0.5,
                        "presence_penalty": 0.5
                    }
                    )


def generate(topic, length, temperature, genre=None, narrative_perspective=None, character_name=None, character_description=None, setting_description=None):
    generation_system_message_content = """
    You are a creative and imaginative assistant specialized in generating stories. 
    When given a prompt, you will generate an engaging and coherent story based on the specified genre and length.
    Your stories should be vivid, imaginative, and suitable for the specified genre. Be sure to maintain a consistent theme and style.
    """

    # Base human message content
    human_message_content = f"""
    Please generate a story based on the following prompt: "{topic}".
    The completion should be approximately `{length}` length.
    """

    # Append optional parameters if they are provided with more explanation
    if genre:
        human_message_content += f"\nThe story should be in the {genre} genre."
    if narrative_perspective:
        human_message_content += f"\nThe story should be narrated from a {narrative_perspective} perspective."
    if character_name:
        human_message_content += f"\nThe main character's name should be {character_name}."
    if character_description:
        human_message_content += f"\nThe main character should be described as: {character_description}."
    if setting_description:
        human_message_content += f"\nThe setting of the story should be described as: {setting_description}."

    human_message_content += "\n **Response Guidelines**: Don't write additional text before after the completion. We already know that you have written story. Only focus on story."

    # Construct the prompt
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=generation_system_message_content),
        HumanMessage(content=human_message_content),
    ])

    response = completion(prompt=prompt_template, topic=topic, length=length, temperature=0.7, genre=None,
                          narrative_perspective=None, character_name=None, character_description=None, setting_description=None)
    return response


def complete(partial_story, length, temperature, genre=None, narrative_perspective=None, character_name=None, character_description=None, setting_description=None):
    completion_system_message_content = """
    You are a creative and imaginative assistant specialized in completing stories. 
    When given a partial story, you will complete it in the same style and tone, ensuring the story flows naturally.
    Your completions should be vivid, imaginative, and suitable for the specified genre. Be sure to maintain the theme and style consistent with the given partial story.
    """

    human_message_content = f"""
    Please complete the following story: `{partial_story}`.
    The completion should be approximately `{length}` length.
    """

    # Append optional parameters if they are provided with more explanation
    if genre:
        human_message_content += f"\nThe story should be in the {genre} genre."
    if narrative_perspective:
        human_message_content += f"\nThe story should be narrated from a {narrative_perspective} perspective."
    if character_name:
        human_message_content += f"\nThe main character's name should be {character_name}."
    if character_description:
        human_message_content += f"\nThe main character should be described as: {character_description}."
    if setting_description:
        human_message_content += f"\nThe setting of the story should be described as: {setting_description}."

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=completion_system_message_content),
        HumanMessage(content=human_message_content)
    ])

    # formatted_prompt = prompt_template.format(
    #     partial_story=partial_story,
    #     length=length,
    #     genre=genre,
    #     paragraphs=paragraphs
    #
    # print(formatted_prompt)

    response = completion(prompt=prompt_template, topic=partial_story, length=length, temperature=0.7, genre=None,
                          narrative_perspective=None, character_name=None, character_description=None, setting_description=None)
    return response


def completion(prompt, topic, length, temperature=0.7, genre=None, narrative_perspective=None, character_name=None, character_description=None, setting_description=None):
    llm = chat_model(temperature)
    llm_chain = prompt | llm

    # Construct the parameters dictionary
    parameters = {
        "topic": topic,
        "length": length,
        "genre": genre,
        "narrative_perspective": narrative_perspective,
        "character_name": character_name,
        "character_description": character_description,
        "setting_description": setting_description
    }

    # Remove None values from parameters
    parameters = {k: v for k, v in parameters.items() if v is not None}
    print(parameters)
    response = llm_chain.invoke(parameters).content
    return response
