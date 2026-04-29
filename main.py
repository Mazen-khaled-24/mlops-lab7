from langgraph.graph import StateGraph, END
from typing import TypedDict


# STATE (Memory)
class AgentState(TypedDict):
    topic: str
    research: str
    draft: str
    review: str
    next_step: str



# AGENTS
def researcher(state: AgentState):
    print(" Researcher working...")
    return {
        "research": f"Research about {state['topic']}",
        "next_step": "supervisor"
    }


def writer(state: AgentState):
    print(" Writer working...")
    return {
        "draft": f"Article: {state['research']}",
        "next_step": "supervisor"
    }


def reviewer(state: AgentState):
    print(" Reviewer checking...")

    if "Research" in state["draft"]:
        decision = "approved"
    else:
        decision = "rejected"

    return {
        "review": decision,
        "next_step": "supervisor"
    }



# SUPERVISOR (REAL ROUTER)
def supervisor(state: AgentState):
    print(" Supervisor deciding...")

    # First step → go to researcher
    if state["research"] == "":
        return {"next_step": "researcher"}

    # After research → go to writer
    if state["draft"] == "":
        return {"next_step": "writer"}

    # After writing → go to reviewer
    if state["review"] == "":
        return {"next_step": "reviewer"}

    # Decision
    if state["review"] == "approved":
        return {"next_step": "end"}
    else:
        return {"next_step": "writer"}  # loop



# GRAPH
builder = StateGraph(AgentState)

builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)
builder.add_node("supervisor", supervisor)


builder.set_entry_point("supervisor")


builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_step"],
    {
        "researcher": "researcher",
        "writer": "writer",
        "reviewer": "reviewer",
        "end": END
    }
)


builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("reviewer", "supervisor")

graph = builder.compile()



user_topic = input("Enter a topic: ")

result = graph.invoke({
    "topic": user_topic,
    "research": "",
    "draft": "",
    "review": "",
    "next_step": ""
})

print("\n FINAL RESULT:")
print(result)