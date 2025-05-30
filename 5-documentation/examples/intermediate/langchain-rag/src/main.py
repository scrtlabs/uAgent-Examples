from agents.langchain_rag_agent import agent
from agents.langchain_rag_user import user
from uagents import Bureau

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    print(f"Adding RAG agent to Bureau: {agent.address}")
    bureau.add(agent)
    print(f"Adding user agent to Bureau: {user.address}")
    bureau.add(user)
    bureau.run()
