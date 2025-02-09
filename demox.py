import chainlit as cl

# Function to set the UI direction based on language
def set_ui_direction(language):
    if language == "Arabic":
        cl.set_config({"direction": "rtl"})
    else:
        cl.set_config({"direction": "ltr"})



@cl.step(type="tool")
async def tool():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"

cl.Config.default_language = "en-US"

@cl.on_message  # this function will be called every time a user inputs a message in the UI

async def on_message(msg: cl.Message):
    if msg.type == "setLanguage":
        language = msg.args.get("language")
        if language == "Arabic":
            cl.set_config({"direction": "rtl"})
        else:
            cl.set_config({"direction": "ltr"})
        await cl.Message(content=f"Language set to {language}.").send()

async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """


    # Call the tool
    tool_res = await tool()

    await cl.Message(content=tool_res).send()



@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Morning routine ideation",
            message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
            icon="/idea.svg",
            ),
        cl.Starter(
            label="Explain superconductors",
            message="Explain superconductors like I'm five years old.",
            icon="/learn.svg",
            ),
        cl.Starter(
            label="Python script for daily email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/terminal.svg",
            ),
        cl.Starter(
            label="Text inviting friend to wedding",
            message="Write a text asking a friend to be my plus-one at a wedding next month. I want to keep it super short and casual, and offer an out.",
            icon="/write.svg",
            )
        ]
# ...


@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    return [
        cl.ChatProfile(
            name="My Chat Profile",
            icon="https://picsum.photos/250",
            markdown_description="The underlying LLM model is **GPT-3.5**, a *175B parameter model* trained on 410GB of text data.",
            starters=[
                cl.Starter(
                    label="Morning routine ideation",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="/idea.svg",
                ),
                cl.Starter(
                    label="Explain superconductors",
                    message="Explain superconductors like I'm five years old.",
                    icon="/learn.svg",
                ),
            ],
        ),
        cl.ChatProfile(
            name="My Arabic Chat Profile",
            icon="https://picsum.photos/250",
          markdown_description="النموذج اللغوي الأساسي هو **GPT-3.5**، وهو *نموذج يحتوي على 175 مليار معامل* تم تدريبه على 410 جيجابايت من البيانات النصية.",
          starters=[
            cl.Starter(
                label="تصميم روتين صباحي، من فضلك!",
                message="هل يمكنك مساعدتي في إنشاء روتين صباحي مخصص يساعد على زيادة إنتاجيتي طوال اليوم؟ ابدأ بسؤالي عن عاداتي الحالية وما هي الأنشطة التي تمنحني الطاقة في الصباح.",
            ),
             cl.Starter(
                label="شرح الموصلات الفائقة",
                message="اشرح لي الموصلات الفائقة وكأنني طفل في الخامسة من عمري.",
                icon="/learn.svg",
            ),
          ],
        ),
    ]

@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "prompt_history",
        "",
    )




# List of available languages
languages = ["English", "Arabic", "French", "Spanish"]

# Function to set the UI direction based on language
def set_ui_direction(language):
    if language == "Arabic":
        cl.set_config({"direction": "rtl"})
    else:
        cl.set_config({"direction": "ltr"})

@cl.on_chat_start
async def start():
    # Show the language selection dropdown
    await cl.Select(
        label="Select Language",
        options=languages,
        placeholder="Choose a language",
        key="language_selection"
    ).send()

@cl.on_message
async def on_message(message: str):
    # Check if the message is a language selection
    if message in languages:
        set_ui_direction(message)
        await cl.Message(content=f"Language set to {message}.").send()
    else:
        await cl.Message(content="Please select a valid language from the dropdown.").send()
