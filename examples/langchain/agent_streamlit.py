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
from typing import List

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.lightdash.client import LightdashClient

# from typing_extensions import TypedDict

class LightdashOpsWorkflowState(AgentState):
    """The state of the agent"""
    # messages: List[AnyMessage]
    user_input_history: List[str]
    call_tools: bool
    raw_response: str
    formatted_response: str


def get_initial_state() -> LightdashOpsWorkflowState:
    """Get the initial state of the agent"""
    print("============== initial state")
    return LightdashOpsWorkflowState(
        messages=[],
        user_input_history=[],
        need_refine=False,
        raw_response="",
        formatted_response="",
    )

def update_state(state: LightdashOpsWorkflowState, user_input: str) -> LightdashOpsWorkflowState:
    """Update the state with the user input"""
    state["messages"].append(HumanMessage(content=user_input))
    # remove empty AI messages
    # state["messages"] = [
    #   message for message in state["messages"]
    #   if not (isinstance(message, AIMessage) and message.content == "")
    # ]
    return state


class ReviewOutput(BaseModel):
    """The output of the review response"""
    solution: str = Field(..., description="The solution to resolve issues responded by the tools")
    answer: str = Field(..., description="The answer to the user's question")
    question: str = Field(..., description="The question to the user's question to clarify")


class FormatResponseOutput(BaseModel):
    """The output of the format response"""
    formatted_response: str = Field(..., description="The formatted response to the user's question")


def get_last_ai_message(messages: List[AnyMessage]) -> AIMessage:
    """Get the last AI message from the messages"""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return message
    raise ValueError("No AI message found in the messages")


class LightdashOpsWorkflow:
    def __init__(self, lightdash_client: LightdashClient, llm: ChatGoogleGenerativeAI):
        self.lightdash_client = lightdash_client
        self.llm = llm  # Store the LLM instance for later use
        self.tools = get_all_readable_tools(lightdash_client=lightdash_client)

    def get_graph_builder(self) -> StateGraph:
        """Get the graph builder for the agent"""
        graph_builder = StateGraph(LightdashOpsWorkflowState)
        # Add the nodes to the graph
        tool_agent_node = self.tool_agent_node()
        graph_builder.add_node("tool_agent", tool_agent_node)
        graph_builder.add_node("review_agent", self.review_node)
        # graph_builder.add_node("format_response_agent", self.format_response_node)
        # Add the edges to the graph
        graph_builder.set_entry_point("tool_agent")
        graph_builder.add_edge("tool_agent", "review_agent")
        graph_builder.add_conditional_edges(
            "review_agent",
            self.should_continue,
            {
                True: "tool_agent",
                False: END,
            }
        )
        # graph_builder.add_edge("format_response_agent", END)
        return graph_builder

    def should_continue(self, state: LightdashOpsWorkflowState) -> bool:
        """Check if the agent should continue"""
        return state["call_tools"]

    def tool_agent_node(self):
        """Create the tool agent node"""
        system_prompt = textwrap.dedent("""\
            You are a helpful assistant that can use tools to get the data from Lightdash.
            You will use the tools to get the data and return the response to the user.

            If you reach the final output, you will set the raw_response to the response.
            Ensure that all required keys are present in the state schema, including 'remaining_steps'.
            """.strip())
        return create_react_agent(
            self.llm,
            self.tools,
            state_modifier=system_prompt,
            state_schema=LightdashOpsWorkflowState,
        )

    def review_node(self, state: LightdashOpsWorkflowState) -> LightdashOpsWorkflowState:
        """Create the review node"""
        # Call the LLM with the messages
        messages = [
            SystemMessage(content=textwrap.dedent("""\
                You are an expert reviewer tasked with evaluating the effectiveness of the current response to the user's inquiry.
                Utilize the available tools to gather relevant data and formulate a thorough response.

                Your evaluation should follow these guidelines:

                1. If the response sufficiently answers the user's question, populate the `answer` field with the response.
                2. If the response is insufficient, indicate further action is needed.
                3. If additional clarification is required, assign the clarification question to the `question` field.

                Ensure that if the response is satisfactory, `call_tools` is set to `False`. Conversely, if it is inadequate, set `call_tools` to `True`.
                If the response does not have the necessary tools for data retrieval, also set `call_tools` to `False`, as data cannot be retrieved without the appropriate tools.

                If the response is found wanting, please be mindful of the following common pitfalls:

                ## Common Pitfalls
                1. Always use the project UUID instead of the project name when retrieving data.
                   It may be helpful to fetch all projects to determine the project UUID from the project name.
                2. Always use the user UUID instead of the user name when retrieving data.
                   It may be helpful to fetch all users to determine the user UUID from the user name.
            """.strip())),
            get_last_ai_message(state["messages"]),
            HumanMessage(content=state["user_input_history"][-1]),
        ]
        response = self.llm.with_structured_output(ReviewOutput).invoke(messages)
        print("============: review_node")
        print(response)
        if not isinstance(response, ReviewOutput):
            raise ValueError(f"Unexpected result type from LLM: {response}")

        # Update the state
        state["call_tools"] = True if len(response.solution) > 0 else False
        # Append the solution to the messages if the call_tools is True
        if state["call_tools"]:
            state["messages"].append(AIMessage(content=response.solution))
        else:
            state["raw_response"] = response.answer if response.answer else response.question
        return state

    def format_response_node(self, state: LightdashOpsWorkflowState) -> LightdashOpsWorkflowState:
        """Format the response node"""
        if not state["raw_response"] or state["raw_response"] == "":  # Ensure there is a message to process
            raise ValueError("No messages to format.")
        messages = [
            SystemMessage(content=textwrap.dedent("""\
                You are a skilled response formatter tasked with enhancing the clarity and presentation of the user's answer.
                Your goal is to ensure that the response is well-structured, concise, and directly addresses the user's question.
                For instance, it might be good to create a table or a list to make the response more readable.
            """.strip())),
            state["raw_response"],
        ]
        print(messages)
        response = self.llm.with_structured_output(FormatResponseOutput).invoke(messages)
        if isinstance(response, FormatResponseOutput):
            # Update the state
            state["formatted_response"] = response.formatted_response
        else:
            raise ValueError("Unexpected result type from LLM.")
        return state


def create_agent(lightdash_client: LightdashClient, llm: ChatGoogleGenerativeAI):
    """Create the agent with the tools"""
    return create_react_agent(llm, get_all_readable_tools(lightdash_client=lightdash_client))


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
        st.session_state.state = None

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
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_ai_token)

    # Create workflow
    if st.session_state.state is None:
        st.session_state.state = get_initial_state()
    memory = MemorySaver()
    agent = create_react_agent(
      llm,
      get_all_readable_tools(lightdash_client=client),
      checkpointer=memory,
      state_modifier=textwrap.dedent("""\
        You are a helpful assistant that can use tools to get the data from Lightdash.
        You will use the tools to get the data and return the response to the user.

        The response should be in the markdown format.

        There are some common pitfalls to be aware of when using the tools:

        ## Common Pitfalls
        1. Always use the project UUID instead of the project name when retrieving data.
            It may be helpful to fetch all projects to determine the project UUID from the project name.
        2. Always use the user UUID instead of the user name when retrieving data.
            It may be helpful to fetch all users to determine the user UUID from the user name.
        """.strip()),
      )

    st.header("Chat with LLM")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Always show chat input at the bottom
    user_input = st.chat_input("Enter your question:", key="question")

    # Generate assistant response
    if user_input:
        # Update state
        print("============: state (before)")
        print(st.session_state.state)
        update_state(st.session_state.state, user_input=user_input)
        print("============: state (after)")
        print(st.session_state.state)
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
                events = agent.stream(st.session_state.state, config, stream_mode="values")
                messages = []
                for event in events:
                    # Log workflow messages
                    last_message = event["messages"][-1]
                    st.session_state.logs.append(last_message)
                    messages.append(last_message)
                response = messages[-1].content if len(messages) > 0 else ""
                # # Retrieve the formatted response
                # snapshot_state = agent.get_state(config=config)
                # response = snapshot_state.values.get("raw_response", "")
                # Append assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": response})
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.success("Response received:")
                # Get the latest state
                st.session_state.state = agent.get_state(config=config).values
                print("============: snapshot state")
                print(st.session_state.state)
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
