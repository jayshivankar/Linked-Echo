import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_text(text):
    # Remove broken surrogate pairs and unsupported Unicode characters
    return text.encode('utf-8', 'surrogatepass').decode('utf-8', 'replace')



def process_posts(raw_file_path,processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path,encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)




def extract_metadata(post):
    template = """
    You are given a LinkedIn post. Your task is to extract metadata in **pure JSON format only**, without any explanation or extra text.

    Instructions:
    - Return **only** a JSON object.
    - Keys: `line_count` (integer), `language` ("English" or "Hinglish"), `tags` (list of max 2 strings).
    - Do not include any preamble or explanation.

    Output example:
    {{
      "line_count": 5,
      "language": "English",
      "tags": ["career", "motivation"]
    }}

    Here is the post:
    {post}
    """

    post = clean_text(post)  # Clean it first

    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    try:
        response = chain.invoke({'post': post})       # Executes a llm chain with the input variable post.
        json_parser = JsonOutputParser()             #  Expects the LLM to return a JSON-formatted string.
        return json_parser.parse(response.content)     # Parses the raw string to a Python dict.
    except OutputParserException as e:
        print("⚠️ Parsing failed. LLM response:", response.content)
        return None


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  # Add the tags to the set

    unique_tags_list = ','.join(unique_tags)

    template = """You will be given a list of tags. You must unify them and output only a JSON object.

    Requirements:
    1. Unify similar tags into broader concepts (e.g. "Job Hunting", "Jobseekers" → "Job Search")
    2. Follow title case for all final tag names (e.g. "Career Development", not "career development")
    3. Tags are unified and merged to create a shorter list. 
    Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
    Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
    Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
    Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    4. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    5. Output a JSON object mapping original tags to the unified tags.
    6. ❗Return ONLY the JSON — no explanation, no formatting, no text before or after.

    Input tags:
    {tags}
    """

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res



if __name__== "__main__":
    process_posts("data/raw_posts.json","data/processed_posts.json")
