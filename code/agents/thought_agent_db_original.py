# initialise a class named ThoughtAgent which is an autogen groupchat. it has functions of run, create_groupchat, continue groupchat and so on
import autogen

from agents.groupchat import GroupChat
from agents.agent import Agent
from agents.prompts.thought_agent_original.research_planner_agent import research_planner_agent

# from agents.prompts.thought_agent_original.research_planner_agent_fire import research_planner_agent
# from agents.prompts.thought_agent_original.firecrawl_websearch_agent import firecrawl_websearch_agent
from agents.prompts.thought_agent_original.send_user_msg_agent import send_user_msg_agent
# from agents.prompts.thought_agent_original.call_firecrawl_websearch_agent import call_firecrawl_websearch_agent
from agents.prompts.thought_agent_original.user_proxy_agent import user_proxy_agent
from agents.prompts.thought_agent_original.coder_agent import coder_agent
from agents.prompts.thought_agent_original.code_executor_agent import code_executor_agent

from agents.prompts.thought_agent_original.expert_knowledge_agent import expert_knowledge_agent
from agents.prompts.thought_agent_original.db_search_and_crawl_agent import db_search_and_crawl_agent

from agents.tools.webcrawl import firecrawl_search_tool
from agents.prompts.prompts import thought_agent_final_message_format

print("res planner: ", research_planner_agent["description"])

class ThoughtAgent():
    def __init__(self, working_dir=None):
        super().__init__()
        
        # Store working directory for this thought agent
        self.working_dir = working_dir

        # Initialise agents using parameter dictionaries from prompts
        self.user_proxy_agent = Agent(**user_proxy_agent)
        self.send_user_msg_agent = Agent(**send_user_msg_agent)
        self.research_planner_agent = Agent(**research_planner_agent)
        # self.firecrawl_websearch_agent = Agent(**firecrawl_websearch_agent)
        # self.call_firecrawl_websearch_agent = Agent(**call_firecrawl_websearch_agent)
        
        # Use custom working directory if provided
        if working_dir:
            from agents.prompts.thought_agent_original.coder_agent import get_coder_agent_config
            from agents.prompts.thought_agent_original.code_executor_agent import get_code_executor_agent_config
            self.coder_agent = Agent(**get_coder_agent_config(working_dir))
            self.code_executor_agent = Agent(**get_code_executor_agent_config(working_dir))
        else:
            self.coder_agent = Agent(**coder_agent)
            self.code_executor_agent = Agent(**code_executor_agent)
        
        self.expert_knowledge_agent = Agent(**expert_knowledge_agent)
        self.websearch_and_crawl_agent = Agent(**db_search_and_crawl_agent)


        # register any tools required by the agents
        # self.firecrawl_websearch_agent.agent.register_for_llm(
        #     name=firecrawl_search_tool["name"], 
        #     description=firecrawl_search_tool["description"]
        # )(firecrawl_search_tool["run_function"])

        # self.call_firecrawl_websearch_agent.agent.register_for_execution(
        #     name=firecrawl_search_tool["name"]
        # )(firecrawl_search_tool["run_function"])

        # Create a group chat with the agents
        # Use custom log directory if working_dir is set
        log_dir = None
        if working_dir:
            import os
            log_dir = os.path.join(working_dir, "groupchat_logs")
            os.makedirs(log_dir, exist_ok=True)
        
        self.groupchat = GroupChat(agents_list=[
                self.user_proxy_agent.agent,
                self.send_user_msg_agent.agent,
                self.research_planner_agent.agent,
                # self.firecrawl_websearch_agent.agent,
                # self.call_firecrawl_websearch_agent.agent,
                self.coder_agent.agent,
                self.code_executor_agent.agent,
                self.expert_knowledge_agent.agent,
                self.websearch_and_crawl_agent.agent
            ], 
            initiator_agent=self.user_proxy_agent.agent,
            last_message_agent=self.send_user_msg_agent.agent,
            custom_speaker_selection_func=self.custom_speaker_selection_func,
            log_directory=log_dir,  # Pass custom log directory
            manager_initial_msg=(
                "You are a team of agents collaborating on the user's query. "
                "Research planner agent is the main agent which decides what to do next. Based on output of research planner agent, call other agents. The next agent to call should be the one told by research planner agent."
                "Never call send user message agent without calling coder agent. calling coder agent is very vrey important."
                
            ),
        )



    def run(self, starting_msg):
        try:
            final_response, messages, summary = self.groupchat.run(starting_msg)
        except Exception as e:
            print(f"[ThoughtAgent] Error in groupchat.run(): {e}")
            final_response = None
            messages = []
            summary = None

        # Handle None values gracefully to prevent concatenation errors
        final_response = str(final_response) if final_response is not None else "No response generated due to execution error"
        summary = str(summary) if summary is not None else "Execution completed with errors"
        
        
        # Collect intermediates from custom agents
        agent_intermediates = {
            "tool_invocations": [],
            "rag_queries": []
        }
        
        # Get tool invocations from websearch_and_crawl_agent
        if hasattr(self.websearch_and_crawl_agent.agent, 'get_tool_invocations'):
            agent_intermediates["tool_invocations"] = self.websearch_and_crawl_agent.agent.get_tool_invocations()
        
        # Get RAG queries from expert_knowledge_agent
        if hasattr(self.expert_knowledge_agent.agent, 'get_rag_queries'):
            agent_intermediates["rag_queries"] = self.expert_knowledge_agent.agent.get_rag_queries()
        
        formatted_response = thought_agent_final_message_format.format(
            final_response=str(final_response),
            summary=str(summary)
        )
        
        # Return the log filename from groupchat
        log_filename = getattr(self.groupchat, 'log_filename', None)
        
        return formatted_response, log_filename, agent_intermediates
    def create_groupchat(self):
        pass
    
    def continue_groupchat(self):
        pass

    def custom_speaker_selection_func(self, last_speaker, groupchat):
        if last_speaker == self.send_user_msg_agent.agent:
            return None
        if last_speaker == self.user_proxy_agent.agent:
            return self.research_planner_agent.agent
        # if last_speaker == self.firecrawl_websearch_agent.agent:
            # return self.call_firecrawl_websearch_agent.agent
        if last_speaker == self.coder_agent.agent:
            return self.code_executor_agent.agent
        return "auto"
