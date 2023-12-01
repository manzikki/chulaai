"""
This program teaches a LLM about our faculty.
Marko Niinimaki 2023
"""
#pip install farm-haystack[colab,inference]

from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import build_pipeline, add_example_data, print_answers
from haystack.utils import fetch_archive_from_http
import os
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

# We are model agnostic :) Here, you can choose from: "anthropic", "cohere", "huggingface", and "openai".
provider = "huggingface"
API_KEY = "XXXXXXXXXXXXXXXXX" # ADD YOUR KEY HERE

doc_dir = "data"

#fetch_archive_from_http(
#    url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip",
#    output_dir=doc_dir,
#)

document_store = InMemoryDocumentStore(use_bm25=True)
files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]

indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

pipe = ExtractiveQAPipeline(reader, retriever)

prediction = pipe.run(
    query="Who is Pietro Borsano", params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
)

from haystack.utils import print_answers

print_answers(prediction, details="minimum")  ## Choose from `minimum`, `medium`, and `all`
