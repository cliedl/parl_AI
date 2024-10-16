# Electify: Helping voters make an informed decision in the 2024 European Elections

# Overview
Electify is an interactive app designed to empower voters with clear, concise summaries of political party positions for the 2024 European Elections. We use Retrieval-Augmented Generation (RAG) to extract relevant information from party manifestos and debates, providing users with an overview of each party's position on any given topic. Find background information on our [organization page]([https://github.com/electify-eu]).

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
You can [watch a walkthrough video](https://www.loom.com/share/f192bc1873fb464686ad456253a5dff2) or try the app yourself at [electify.eu](https://electify.eu), where it will be deployed until the European Elections in June 2024. We welcome your feedback.

# Local setup
To set up Electify locally, follow the steps below:

[Download database from google drive](https://drive.google.com/drive/folders/161BfV8sTnFMX7AjjBx1qHVaHwnNWEYEO?usp=sharing).
You can also recreate the database using RAG/scripts/create_databases.ipynb, but it is very time-consuming. 
Copy the databases into the data folder.

```
git clone https://github.com/europarl-ai/europarl-ai.git

cd europarl-ai
```

Choose one of the following options to set up the environment:

## Option 1: Docker
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

## Option 2: Build the environment manually

Create an environment with Python 3.11, for example with conda:
```
conda create -n electify python=3.11
conda activate electify
```

Install required packages:
```
pip install -r requirements.txt
```

Run the Streamlit app:
```
streamlit run App.py
```
