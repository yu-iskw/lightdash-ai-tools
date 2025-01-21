# Copyright 2025 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import textwrap

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.lightdash.client import LightdashClient

# from typing_extensions import TypedDict

def get_initial_state() -> AgentState:
    """Get the initial state of the agent"""
    return AgentState(
        messages=[],
        is_last_step=False,
        remaining_steps=0,
        structured_response=None,
    )

def update_state(state: AgentState, user_input: str) -> AgentState:
    """Update the state with the user input"""
    state.messages.append(HumanMessage(content=user_input.strip()))
    return state


def main():
    # Load environment variables
    load_dotenv()

    st.title("Lightdash Agent Interface")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "state" not in st.session_state:
        st.session_state.state = get_initial_state()

    # Input fields for sensitive information in the sidebar
    with st.sidebar:
        with st.container(key="config", border=True, height=300):
            lightdash_url = st.text_input("Enter your Lightdash URL:", value=os.getenv("LIGHTDASH_URL", ""))
            lightdash_api_key = st.text_input("Enter your Lightdash API Key:", type="password", value=os.getenv("LIGHTDASH_API_KEY", ""))
            google_ai_token = st.text_input("Enter your Google AI Studio Token:", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        with st.container(key="logs", border=True, height=600):
            if st.session_state.logs:
                for log in st.session_state.logs:
                    st.write(log)
            else:
                st.write("No logs available.")

    # Validate input fields
    if not lightdash_url or not lightdash_api_key or not google_ai_token:
        st.sidebar.error("Please enter your LIGHTDASH_URL, LIGHTDASH_API_KEY, and GOOGLE_AI_TOKEN.")
        return

    # Initialize Lightdash client
    client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
      model="gemini-1.5-flash",
      google_api_key=google_ai_token,
      temperature=0.1)

    # Create workflow
    memory = MemorySaver()
    agent = create_react_agent(
      llm,
      get_all_readable_tools(lightdash_client=client),
      checkpointer=memory,
      state_modifier=textwrap.dedent("""\
        You are an advanced assistant designed to leverage tools for retrieving data from Lightdash efficiently.
        Your primary objective is to utilize these tools to extract relevant information and provide comprehensive responses to user inquiries.
        In cases where the data cannot be retrieved, you should proactively engage the user by prompting them to clarify or refine their question for better results.
        You have to return any content. Don't return empty content.

        Ensure that all responses are formatted in Markdown for clarity and readability.

        Be mindful of the following common pitfalls when using the tools:

        ## Common Pitfalls
        1. Always utilize the project UUID instead of the project name when retrieving data. To find the project UUID, consider fetching all projects first.
        2. Always use the user UUID instead of the user name when retrieving data. It may be beneficial to fetch all users to ascertain the user UUID from the user name.
        """.strip()),
      )

    st.header("Chat with LLM")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate assistant response
    if user_input := st.chat_input("Enter your question:", key="question"):
        # Update state
        update_state(st.session_state.state, user_input=user_input)
        # Append user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        # Generate response
        with st.spinner("Generating response..."):
            try:
                # Initialize workflow state
                config = {
                    "configurable": {"thread_id": "1"},
                    "recursion_limit": 1000,
                }
                # Stream workflow events
                response = ""
                for _ in range(3):
                    if response == "":
                        events = agent.stream(st.session_state.state, config, stream_mode="values")
                        messages = []
                        for event in events:
                            # Log workflow messages
                            last_message = event["messages"][-1]
                            st.session_state.logs.append(last_message)
                            messages.append(last_message)
                        response = messages[-1].content if messages else ""
                if response == "":
                    response = textwrap.dedent("""\
                        I'm sorry, but I couldn't retrieve the data you requested.
                        Please refine your question or provide more details.
                        """.strip())
                # Append assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": response})
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.success("Response received:")
                # Get the latest state
                st.session_state.state = agent.get_state(config=config).values
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
