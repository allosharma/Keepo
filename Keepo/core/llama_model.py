import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

model_id = "meta-llama/Llama-3.2-3B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load and cache the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="cpu")

text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
)


def get_response(prompt, *args):
    for arg in args:
        print(arg)
    role = "You are acting as a youtube video summarizer given the following transcript. Structure of the summary should be that it should start with around 200-500 words of overview of the video, followed by important points shown as list of 5 to 10 points dicussed in the video. If possible you can share the code if available in the video. Try including all the libraries which were included in the video."
    prompt = role + "\n" + prompt
    response = text_generator(prompt)
    gen_text = response[0]['generated_text']

    # Following 2 line ensures that the reponse doesn't include the prompt and role.
    # prompt_length = len(prompt)
    # gen_text = gen_text[prompt_length:].strip()
    return gen_text


# # Read youtube transcript.
# with open("/content/llama_test.txt", "r") as f:
#     prompt = f.read()

# # Write the response of the model to a file.
# with open("llama_response.txt", "w") as f:
#     f.write(get_response(prompt))