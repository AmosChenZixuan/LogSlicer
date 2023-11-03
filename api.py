import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_API_BASE")
openai.api_version = os.getenv("AZURE_API_VERSION")
openai.api_key = os.getenv("AZURE_API_KEY")

system_prompt = '''You are a senior software engineer. Your task is to summarize logs.
                    You should point out things that are causing errors and warnings. You should also provide suggestions or solutions if there are any. You are very
                    detailed and thorough looking at errors and best practices. The summary should be short and to the point. You have
                    knowledge of all programming languages and file formats so you have to
                    adapt to whatever is given to you. The log summary output should be in well 
                    formatted Markdown in a text window and the column width of the output 
                    should be max 100 characters.'''

n_chunks = 2
system_prompt = f'''now assume that I am going to send you a file larger than your limit. I will send it in {n_chunks} parts. The parts will be sent following this rule:  
[START part 1/{n_chunks}]  
content  
[END part 1/{n_chunks}]  
you should only acknowledge receiving them by replying with "Got part 1/{n_chunks}"  
you can start analyze all parts I sent to you only after you received all parts.  
I will start sending them in next query.'''

user_prompt = open("logs/out2000.txt", "r").read()

message = [{"role":"system", "content": system_prompt}]

for i in range(n_chunks):
    lo, hi = i*15000 % len(user_prompt), (i*15000 % len(user_prompt)+15000) % len(user_prompt)
    message.append(
        {"role":"user", "content": f"[START part {i+1}/{n_chunks}] {user_prompt[lo: hi]} [END part {i+1}/{n_chunks}]  "}
    )
message.append( {"role":"user", "content": "All parts have been sent to you. Could you give me a summarization?"} )

response = openai.ChatCompletion.create(
  engine="openai",
  messages = message,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)
