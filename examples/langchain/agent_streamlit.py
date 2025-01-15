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
    need_refine: bool
    raw_response: str
    formatted_response: str


def get_initial_state(initial_user_input: str) -> LightdashOpsWorkflowState:
    """Get the initial state of the agent"""
    return {
      "messages": [
        HumanMessage(content=initial_user_input),
        ],
      "user_input_history": [initial_user_input],
      "need_refine": False,
      "raw_response": "",  # Added raw_response to match the TypedDict
      "formatted_response": "",
      }


class ReviewOutput(BaseModel):
    """The output of the review response"""
    solution: str = Field(..., description="The solution to the user's question")
    need_refine: bool = Field(..., description="Whether the solution needs to be refined")


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
        graph_builder.add_node("format_response_agent", self.format_response_node)
        # Add the edges to the graph
        graph_builder.set_entry_point("tool_agent")
        graph_builder.add_edge("tool_agent", "review_agent")
        graph_builder.add_conditional_edges(
            "review_agent",
            self.should_continue,
            {
                True: "tool_agent",
                False: "format_response_agent",
            }
        )
        graph_builder.add_edge("format_response_agent", END)
        return graph_builder

    def should_continue(self, state: LightdashOpsWorkflowState) -> bool:
        """Check if the agent should continue"""
        return state["need_refine"]

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
                You are a helpful reviewer to check if the current response answers the user's question.

                If the response is enough, you will set the need_refine to False.
                Otherwise, you will set the need_refine to True.
                And, if it lacks tools to get the data, you will set the need_refine to False too.
                That's because it is not possible to get the data without extra tools.

                If the response is not enough, you will think of the solution to avoid the following pitfalls.

                ## Common Pitfalls
                - We have to pass the project UUID, not the project name, to get the data.
                  So, it might be good to get all the projects so that we can identify the project UUID from the project name.
                - We have to pass the user UUID, not the user name, to get the data.
                  So, it might be good to get all the users so that we can identify the user UUID from the user name.
            """.strip())),
            state["messages"][-1]
        ]
        response = self.llm.with_structured_output(ReviewOutput).invoke(messages)
        if isinstance(response, ReviewOutput):
            # Update the state
            state["need_refine"] = response.need_refine
            # Append the solution to the messages if the need_refine is True
            if response.need_refine:
              state["messages"].append(AIMessage(content=response.solution))
        else:
            raise ValueError("Unexpected result type from LLM.")
        return state

    def format_response_node(self, state: LightdashOpsWorkflowState) -> LightdashOpsWorkflowState:
        """Format the response node"""
        if not state["raw_response"]:  # Ensure there is a message to process
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
    # load env
    load_dotenv()

    st.title("Lightdash Agent Interface")

    # Create tabs for chat and logs
    chat_tab, logs_tab = st.tabs(["Chat with LLM", "Workflow Logs"])

    # Input fields for sensitive information in the sidebar
    with st.sidebar:
        lightdash_url = st.text_input("Enter your Lightdash URL:", value=os.getenv("LIGHTDASH_URL", ""))
        lightdash_api_key = st.text_input("Enter your Lightdash API Key:", type="password", value=os.getenv("LIGHTDASH_API_KEY", ""))
        google_ai_token = st.text_input("Enter your Google AI Studio Token:", type="password", value=os.getenv("GOOGLE_API_KEY", ""))  # New field for Google AI token

    # Use st.chat_input for the question input in the chat tab
    with chat_tab, logs_tab:
        question = chat_tab.chat_input("Enter your question:")

        # Create Lightdash client
        if not lightdash_url or not lightdash_api_key or not google_ai_token:  # Check for Google AI token
            st.error("Please enter your LIGHTDASH_URL, LIGHTDASH_API_KEY, and GOOGLE_AI_TOKEN.")
            return

        client = LightdashClient(
            base_url=lightdash_url,
            token=lightdash_api_key,
        )

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_ai_token)
        graph_builder = LightdashOpsWorkflow(client, llm).get_graph_builder()
        memory = MemorySaver()
        workflow = graph_builder.compile(checkpointer=memory)

        if not question:
            chat_tab.warning("Please enter a question to proceed.")
        else:
            init_state = get_initial_state(initial_user_input=question)
            config = {
              "configurable": {"thread_id": "1"},
              "recursion_limit": 1000,
              }
            while True:  # Loop to continue the chat
              with st.spinner("Generating response..."):
                  try:
                    events = workflow.stream(init_state, config, stream_mode="values")
                    response = ""
                    for s in events:
                      # Leave the logs to the workflow log tab
                      last_message = s["messages"][-1]
                      logs_tab.write(last_message)
                    # Get the formatted response from the snapshot state
                    snapsnot_state = workflow.get_state(config=config)
                    print(snapsnot_state)
                    response = snapsnot_state.values.get("formatted_response", "")
                    chat_tab.success("Response received:")
                    chat_tab.chat_message("assistant").markdown(response)
                  except Exception as e:
                    chat_tab.error(f"Error: {e}")

                  # Human-in-the-loop: Ask for user confirmation on the response
                  if next_question := chat_tab.chat_input("Enter your next question:"):  # Prompt for next input
                      question = next_question
                  else:  # Exit loop if no new question is provided
                      chat_tab.warning("Please enter a question to proceed.")
                      break


if __name__ == "__main__":
    main()
