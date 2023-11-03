# Project Name

- LISA (Log Intelligent Summarization Assistant)
- LEXIS (Log Extraction and Intelligent Summarization)
- LITE (Log Intelligent Text Extractor)
- LIGHT - Log Insight/Info Gathering and Highlighting assisTant

# TODO

- LogReader 
    using python-dlt
    support dlt-viewer too, in case dependencies become unavailable
- LogSlicer
    split log into chunks based on size threshold


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