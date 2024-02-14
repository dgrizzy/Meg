# Meg
Meg is an LLM powered data analyst with the ability to self-determine course of action, use tools to query and visualize data in an RDBMS, and synthesize conclusions.

Meg is a Langchain agent built on GPT 3.5 turbo. In this example, Meg has access to a record store's data from the popular development database, [chinook.db](static/chinook_diagram.pdf).

Meg is named after Meg White, the drummer of my favorite Detroit Rock Band, the White Stripes.

## Meg Agent Architecture
Meg is actually just the name of the team leader that you work with. She has a team of two, an analyst responsible for querying the database and an analyst responsible for building data visualizations. Each of them have their own tools, prompts, and scope. Meg is responsible for the overall analysis.

From a technical perspective, this is accomplished by building three agents in Langchain and then orchestrating them together using LangGraph.

LLMs, like us, tend to be best when they have good abstractions, clear expectations, and well structured roles, allowing them to focus on the thing itself. 
