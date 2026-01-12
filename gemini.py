from google import genai
from pathlib import Path
import pandas as pd 
import json

client = genai.Client(api_key="AIzaSyByDCISzyhMtrNSfnI2XF8yq-4g3JfPXEw")

# pdf_path = r"C:\Users\varun.pardeshi\Desktop\tool\Panel AI\Images\CR13 Panel Schedules A.pdf"
# pdf_path2 = r"C:\Users\varun.pardeshi\Desktop\tool\Panel AI\Images\CR13 Panel Schedules A (1).pdf"

IMAGE_DIR = Path(r"C:\Users\varun.pardeshi\Desktop\tool\Panel AI\Images\test\one")
PROMPT_DIR = Path(__file__).resolve().parent /"settings"/ "Prompts"
pdf_files = list(IMAGE_DIR.glob("*.pdf"))

uploaded_files = []
for path in pdf_files:
    print(f"Uploading: {path.name}...")
    uploaded_file = client.files.upload(file=str(path))
    uploaded_files.append(uploaded_file)

def load_prompt(name):
    path = PROMPT_DIR / f"{name}.txt"
    return path.read_text(encoding="utf-8")

circuit = client.models.generate_content(
    model="gemini-2.5-pro", contents=[load_prompt("Circuit_Prompt"), *uploaded_files]
)




df = pd.DataFrame(columns=["customer","location","suite","rack"	,"rating","cir","volts","num_poles","panel","side","room_id","cabinet_watts_rating"])
# circuit = """
# ```json
# [
#     {
#         "Panel Name": "A9-2",
#         "Circuit Numbers": "1, 3, 5",
#         "Rack Name": "RACK 3116",
#         "OCD (Amps)": 60
#     },
#     {
#         "Panel Name": "A9-2",
#         "Circuit Numbers": "2, 4, 6",
#         "Rack Name": "RACK 3117",
#         "OCD (Amps)": 60
#     }
# ]
# ```
# """



new = circuit.text.split('json')
clean_s = new[1].replace("```", "")
clean_s = clean_s.strip()
data_array = json.loads(clean_s)

# print(data_array)


for a in data_array : 
    new_row = {"customer":'',"location": ' ',"suite": '',"rack" :a['Rack Name']	,"rating": a['OCD (Amps)'],"cir" : str(a['Circuit Numbers']),"volts":'',"num_poles":'',"panel":a['Panel Name'],"side":'',"room_id":"","cabinet_watts_rating":''}
    df.loc[len(df)] = new_row

print(df)
df.to_excel("test.xlsx")