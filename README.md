<p align="center">
<img src="assets/logo.png" alt="ThinkAi" style="display: block; margin: auto; background-color: transparent;">
</p>

# ThinkAi

[![Website](https://img.shields.io/badge/Website-Demo-20B2AA.svg)](https://thinkai.live)
[![Code License](https://img.shields.io/badge/Code%20License-MIT-purple.svg)](https://github.com/OptimalScale/LMFlow/blob/main/LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![LangChain](https://img.shields.io/badge/LangChain-0.0.265-darkgreen.svg)](https://www.langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt_3.5_turbo-red.svg)](https://platform.openai.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-meta_bart_large_cnn-yellow.svg)](https://huggingface.co/facebook/bart-large-cnn)
[![NextJS](https://img.shields.io/badge/NextJS-13.4+-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-16+-7cc5d9.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/typeScript-007acc?logo=typescript&logoColor=white&style=flat)](https://www.typescriptlang.org)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-white?&logo=tailwind+css&logoColor=38bdf8&style=flat)](https://tailwindcss.com)

ThinkAi is a Python-based LLM App trained on philosophy research that can answer questions on philosophy using Chroma's Vector Search, HuggingFace tokenizers for text chunking, Meta's `bart-large-cnn` model for summarizing, and OpenAI's `gpt-3.5-turbo` model for structuring the final response. This is wrapped with a NextJS web app, code here - [ThinkAi UI](https://github.com/maanvithag/think-ai-ui)

# Basic User Flow:
Here is how ThinkAi processes each user query;
* User pings the [web client](http://thinkai.live/) with a query.
* Chroma DB creates embeddings for this query
* Using vector search, Chroma DB pulls the closest top 3 articles for the query
* The summaries for these articles is pulled from the preprocessed `JSON` file from below and are combined by simple concatenation
* The combined text is included in prompt for `OpenAI GPT model`
* API call to OpenAI `gpt-3.5-turbo` model and get response
* Response is sent back to the user
<p align="center">
<img src="assets/userflow.png" alt="ThinkAi" style="display: block; margin: auto; background-color: transparent;">
</p>

## Preprocessing Steps
1. [Data Collection](#data-collection)
2. [Create Embeddings](#create-embeddings)
3. [Summarize each article](#summarize)

Code for all the preprocessing step - COMING SOON!

# Preprocessing: Data Collection <a name="data-collection"></a>
All the data has been collected from articles published and owned by [Stanford Encyclopedia of Philosphy](https://plato.stanford.edu). Using `beautifulsoup`, all scraped pages were dumped into files which were then cleaned removing noise like html tags, media, etc. and structured into `JSON` files.
<p align="center">
<img src="assets/datacollection.png" alt="ThinkAi" style="display: block; margin: auto; background-color: transparent;">
</p>

# Preprocessing: Create Embeddings <a name="create-embeddings"></a>
Using [Chroma DB](https://www.trychroma.com), embeddings are created on the entire text of each article with an index on the URL of each article. For a given query, Chroma creates embeddings and then using Vector search, Chroma pulls out the closest top 3 articles for the given query.
<p align="center">
<img src="assets/chromaembeddings.png" alt="ThinkAi" style="display: block; margin: auto; background-color: transparent;">
</p> 

# Preprocessing: Summarize each article <a name="summarize"></a>
There are a lot of summarization models, however, the max token size is at 1024 tokens (~800 words) for summarizing any text. This does not fit the use case since the text here is at least a couple of pages long. One way to work through this is to chunk text, summarize individually, and combine again. This may result in loss of continuity in the flow of the text, to overcome that, we add few tokens overlap in each chunk so we stay with the flow. This has proven to extract the main context of the article. Each `JSON` file is broken into chunks of `1000 tokens` using [LangChain's Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/). These chunks are individually summarized using [Meta's BART model](https://arxiv.org/abs/1910.13461) published on [HuggingFace](https://huggingface.co/facebook/bart-large-cnn). Finally, these individual summaries are combined together by simple concatenation.
<p align="center">
<img src="assets/summarize.png" alt="ThinkAi" style="display: block; margin: auto; background-color: transparent;">
</p>

All the generated summaries for each article is stored in a `JSON` file for fast access.