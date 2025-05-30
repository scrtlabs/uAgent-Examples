from uagents import Agent, Context

agent = Agent(name="alice", seed="alice recovery phrase", port=8000, endpoint=["http://127.0.0.1:8000/submit"])

@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")

if __name__ == "__main__":
    agent.run()