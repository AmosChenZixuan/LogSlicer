import os
import openai
openai.api_type = "azure"
openai.api_base = "https://vlv-openai-uk.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "a6a806d247084cf689348423a6345be4" #os.getenv("OPENAI_API_KEY")

system_prompt = '''You are a senior software engineer. Your task is to summarize logs.
                    You should point out things that are causing errors and warnings. You should also provide suggestions or solutions if there are any. You are very
                    detailed and thorough looking at errors and best practices. The summary should be short and to the point. You have
                    knowledge of all programming languages and file formats so you have to
                    adapt to whatever is given to you. The log summary output should be in well 
                    formatted Markdown in a text window and the column width of the output 
                    should be max 100 characters.'''

system_prompt = '''now assume that I am going to send you a file larger than your limit. I will send it in three parts. The parts will be sent following this rule:  
[START part 1/3]  
content  
[END part 1/3]  
you should only acknowledge receiving them by replying with "Got part 1/3"  
you can start analyze all parts I sent to you only after you received all parts.  
I will start sending them in next query.'''

user_prompt = open("logs/out2000.txt", "r").read()[:28000]

response = openai.ChatCompletion.create(
  engine="openai",
  messages = [
      {"role":"system", "content": system_prompt},
      {"role":"user", "content": ""},
      #{"role":"assistant","content":"Hello! How can I assist you today?"}
      ],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)

response = openai.ChatCompletion.create(
  engine="openai",
  messages = [
      {"role":"system", "content": system_prompt},
      {"role":"user", "content": "[START part 1/3] this part has a number 10 [END part 1/3]  "},
      {"role":"user", "content": "[START part 2/3]  this part has a number 11[END part 2/3]  "},
      {"role":"user", "content": "[START part 3/3] what is the sum of the numbers in previous parts?  [END part 3/3]  "},
      {"role":"user", "content": "All parts have been sent to you. You can now start to analyze them."},
      #{"role":"assistant","content":"Hello! How can I assist you today?"}
      ],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)
