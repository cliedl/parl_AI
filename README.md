# Electify: Helping voters make an informed decision

# Overview
Electify is an interactive app designed to empower voters with clear, concise summaries of political party positions. It was first developed for the 2024 European Elections. We use Retrieval-Augmented Generation (RAG) to extract relevant information from party manifestos and debates, providing users with an overview of each party's position on any given topic. Find background information on our [organization page](https://github.com/electify-eu).

# Contributors

[Chris Liedl](https://github.com/cliedl)

[Anna Neifer](https://github.com/Aneifer)

[Joshua Nowak](https://github.com/josh-nowak)

# Features
- Retrieve relevant information from party manifestos and debates
- Summarize parties' political positions based on user query
- Hide party names to prevent bias
- Show all retrieved sources for transparency

# Demo
You can [watch a walkthrough video](https://www.loom.com/share/f192bc1873fb464686ad456253a5dff2) or try the app yourself at [electify.eu](https://electify.eu).

# Local setup
To set up Electify locally, follow the steps below:

```
git clone https://github.com/europarl-ai/electify-app.git

cd electify-app
```

Choose one of the following options:

## Option 1: Deploy using Docker
Create `.env` file in the repository's root directory containing your OpenAI API key:
```
OPENAI_API_KEY=<value>
```

Run the following commands to build and run the Docker container:
```
docker build -t electify .
docker run -p 8080:8080 --env-file .env electify
```

Navigate to `http://localhost:8080` in your browser to access the app.

## Option 2: Deploy on host machine

Install dependencies, e.g. with [uv](https://docs.astral.sh/uv/getting-started/installation/):
```
uv sync --frozen --no-dev
```

Activate the environment:
```
source .venv/bin/activate
```

Run the Streamlit app:
```
streamlit run App.py
```