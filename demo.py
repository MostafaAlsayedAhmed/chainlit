import chainlit as cl


@cl.step(type="tool")
async def tool():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"

# cl.Config.default_language = "en-US"

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

@cl.on_message
async def on_message(message: cl.Message):
    # Get all the messages in the conversation in the OpenAI format
    print(cl.chat_context.to_openai())

"""
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
            name="ملفي الشخصي في الدردشة العربية",
            icon="https://picsum.photos/250",
          markdown_description="النموذج اللغوي الأساسي هو **GPT-3.5**، وهو *نموذج يحتوي على 175 مليار معامل* تم تدريبه على 410 جيجابايت من البيانات النصية.",
          starters=[
            cl.Starter(
                label="تصميم روتين صباحي، من فضلك!",
                message="هل يمكنك مساعدتي في إنشاء روتين صباحي مخصص يساعد على زيادة إنتاجيتي طوال اليوم؟ ابدأ بسؤالي عن عاداتي الحالية وما هي الأنشطة التي تمنحني الطاقة في الصباح.",
                    icon="/idea.svg",
            ),
             cl.Starter(
                label="شرح الموصلات الفائقة",
                message="اشرح لي الموصلات الفائقة وكأنني طفل في الخامسة من عمري.",
                icon="/learn.svg",
            ),
          ],
        ),  ]


# Reply to a user message
@cl.on_message
async def on_message(message: cl.Message):
    # Get all the messages in the conversation in the OpenAI format
    print(cl.chat_context.to_openai())

    # Send the response
    response = f"Hello, you just sent: {message.content}!"
    await cl.Message(response).send()

# to show the actions list.  # Create an action


@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(
            name="action_button",
            icon="mouse-pointer-click",
            payload={"value": "example_value"},
            label="Here is Action 1"
        ),
        cl.Action(
            name="call_us",
            icon="phone",
            payload={"value": "example_value"},
            label="Call Us!"
        )
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()


@cl.action_callback("action_button")
async def on_action(action):
    await cl.Message(content=f"Executed {action.name}").send()
    # Optionally remove the action button from the chatbot user interface
    await action.remove()


"""
