# Project Name

- LISA (Log Intelligent Summarization Assistant)
- LEXIS (Log Extraction and Intelligent Summarization)
- LITE (Log Intelligent Text Extractor)
- LIGHT - Log Insight/Info Gathering and Highlighting assisTant

# TODO

- write a base class for log file loader, making the dlt loader substitutable
- Documentation
- Docker file


# Strategy

- Time-series 
    batch log into time section and summarize for each
- Unique errors
    list unique errors and rank by frequency


# Setup

```
poetry install
bash setup.sh
```

Start MongoDB
```
sudo mkdir -p data/db
sudo mongod --dbpath ~/data/db
```

```
mongod --fork --config /etc/mongod.conf
```

Start Service
```
uvicorn main:app --reload
```

# Requirements

```
# openai
openai
tiktoken

# CAN log
python-can # read blf file
cantools # read dbc file and parse blf file

# langchain
langchain
sentence-transformer # doc embedding
torch           # dependency of sentence-transformer
scikit-learn    # chunk analysis
matplotlib      # visualization
python-dotenv # loading environment variables e.g. API keys
```

# Trouble Shooting

### Exceeding token limit
- Try gpt4-turbo, which has much larger context window
- Reduce the value of "max_token" parameter of llm
    - this will reduce the length of output
- Reduce the value of "chunk_size" parameter of preprocess.chunk_documents
    - this might increase the number of chunks