# import necessary libraries
import os
import camelot
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import json
from dotenv import load_dotenv

load_dotenv()

# define folder contains brochures
pdf_folder = "./dataset"

# insert your openai api key and llm
os.environ["OPENAI_API_KEY"] = " "
llm = ChatOpenAI(model="gpt-4o-mini")

# function to read pdf documents and write to "table"
def pdf_to_table(pdf_folder):
    table_data_list = []
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
            for i, table in enumerate(tables):
                extracted_text = table.df.to_string()
                source_info = f"{pdf_path}"
                # catch the content and its path source
                table_data_list.append({"text": extracted_text, "source": source_info})
    return table_data_list

# summarize each content in "table"
def summarize_tables(tables):
    summaries = []
    for table_entry in tables:
        prompt = f"Summarize the following table data:\n{table_entry['text']} but answer it in INDONESIAN LANGUAGE"
        #print(table_entry)
        response = llm.invoke([HumanMessage(content=prompt)])
        summaries.append({"summary": response, "source": table_entry["source"]})
    return summaries

# extract the content of summaries
def clean_summarization(summaries):
    cleaned = summaries
    for summary in summaries:
        if isinstance(summary["summary"], AIMessage):
            summary["summary"] = summary["summary"].content  # Extract text
    return cleaned

# convert summary to json
def summary_to_json(summaries):
    save_dir = "./assets" # you can change the directory to save json
    file_name = "docs_indonesian.json" # you can change the json file name
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summaries, f, indent=4)
        print(f"JSON saved successfully at: {file_path}")
    except Exception as e:
        print(f"Error saving JSON: {e}")

# initialize table
table_list = pdf_to_table(pdf_folder)

# variable to catch the summarized table
summaries = summarize_tables(table_list)

# clean and export the summaries to json
cleaned_summaries = clean_summarization(summaries)
summary_to_json(cleaned_summaries)
