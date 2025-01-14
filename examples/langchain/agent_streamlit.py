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
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict

from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.lightdash.client import LightdashClient


class LightdashOptAgentState(TypedDict):
    """The state of the agent"""
    messages: List[AnyMessage]
    user_inputs: List[str]
    need_refine: bool

    @classmethod
    def get_initial_state(cls, initial_user_input: str) -> "LightdashOptAgentState":
        """Get the initial state of the agent"""
        return {"messages": [], "user_inputs": [initial_user_input], "need_fix": False}

class ReviewOutput(BaseModel):
    """The output of the review response"""
    solution: str = Field(..., description="The solution to the user's question")
    need_refine: bool = Field(..., description="Whether the solution needs to be refined")

class LightdashOpsAgent:
    def __init__(self, lightdash_client: LightdashClient, llm: ChatGoogleGenerativeAI):
        self.lightdash_client = lightdash_client
        self.llm = llm  # Store the LLM instance for later use
        self.tools = get_all_readable_tools(lightdash_client=lightdash_client)

    def get_graph_builder(self):
        """Get the graph builder for the agent"""
        graph_builder = StateGraph(LightdashOptAgentState)
        # Add the nodes to the graph
        tool_agent_node = self.tool_agent_node()
        graph_builder.add_node("tool_agent", tool_agent_node)
        graph_builder.add_node("review_agent", self.review_node)
        # Add the edges to the graph
        graph_builder.set_entry_point("tool_agent")
        graph_builder.add_edge("tool_agent", "review_agent")
        graph_builder.add_conditional_edges(
          "review_agent",
          self.should_continue,
          {
            True: "tool_agent",
            False: "END",
          }
        )
        return graph_builder

    def should_continue(self, state: LightdashOptAgentState):
        """Check if the agent should continue"""
        return state["need_refine"]

    def tool_agent_node(self):
        """Create the tool agent node"""
        return create_react_agent(self.llm, self.tools)

    def review_node(self, state: LightdashOptAgentState):
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
        result = self.llm.with_structured_output(ReviewOutput).invoke(messages)
        # Update the state
        state["messages"].append(AIMessage(content=result.solution))
        state["need_refine"] = result.need_refine
        return state


def create_agent(lightdash_client: LightdashClient, llm: ChatGoogleGenerativeAI):
    """Create the agent with the tools"""
    return create_react_agent(llm, get_all_readable_tools(lightdash_client=lightdash_client))

def main():
    # load env
    load_dotenv()

    st.title("Lightdash Agent Interface")

    # Input fields for sensitive information in the sidebar
    with st.sidebar:
        lightdash_url = st.text_input("Enter your Lightdash URL:", value=os.getenv("LIGHTDASH_URL", ""))
        lightdash_api_key = st.text_input("Enter your Lightdash API Key:", type="password", value=os.getenv("LIGHTDASH_API_KEY", ""))
        google_ai_token = st.text_input("Enter your Google AI Studio Token:", type="password", value=os.getenv("GOOGLE_AI_TOKEN", ""))  # New field for Google AI token

    # Use st.chat_input for the question input
    question = st.chat_input("Enter your question:")

    # Create Lightdash client
    if not lightdash_url or not lightdash_api_key or not google_ai_token:  # Check for Google AI token
        st.error("Please enter your LIGHTDASH_URL, LIGHTDASH_API_KEY, and GOOGLE_AI_TOKEN.")
        return None

    client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_ai_token)

    if question:  # Check if question is provided
        graph_builder = LightdashOpsAgent(client, llm).get_graph_builder()
        workflow = graph_builder.compile()
        if workflow:
            while True:  # Loop to continue the chat
                with st.spinner("Generating response..."):
                    messages = [HumanMessage(content=question)]
                    config = {"recursion_limit": 100}
                    response = ""
                    events = workflow.stream({"messages": messages}, config, stream_mode="values")
                    for s in events:
                        message = s["messages"][-1]
                        response += str(message) + "\n" if isinstance(message, tuple) else message.content + "\n"
                    st.success("Response received:")
                    st.text_area("Answer", value=response, height=300)

                    # Human-in-the-loop: Ask for user confirmation on the response
                    if st.button("Confirm Response"):
                        st.success("Response confirmed.")
                        break  # Exit the loop if confirmed
                    else:
                        question = st.chat_input("Enter your next question:")  # Prompt for next input
                        if not question:  # Exit loop if no new question is provided
                            st.warning("Please enter a question to proceed.")
                            break
    else:
        st.warning("Please enter a question to proceed.")

if __name__ == "__main__":
    main()
