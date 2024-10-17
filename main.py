from swarm.repl import run_demo_loop
from agents import SQLAgent

if __name__ == "__main__":
    sql_agent = SQLAgent()
    run_demo_loop(sql_agent.agent, stream=True)
