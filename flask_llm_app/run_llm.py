"""
This file is for feeding the extracted sentences from PDF and feed into llm for answers
"""
import json


def feed_to_model(sentences, model, tokenizer):
    """
    input: [List] sentences,
    model: llm transformer,
    tokenizer
    """
    #responses = {"chemical_info": []}
    responses = []
    chemical_name = set()
    # put the pdf text in a string
    for sentence in sentences:
        # feed each sentence to the model
        prompt = """Extract "chemical_name" (keyword,content) from the text above,
                    also content such as "chemical_property", "chemical_hazard" and output in json format.
                    Do not output anything if there is no chemical name.
                    Skip the citation and reference.
                    Output JSON object only."""

        llm_input = f"{sentence}\n\n{prompt}"
        response, history = model.chat(tokenizer, llm_input, history=[])
        # resolve unused variable
        history = history[0]
        # bypass the invalid output
        if not response.isascii():
            continue
        # load the json output
        try:
            data = json.loads(response)
        except json.decoder.JSONDecodeError:
            print("cannot load json")
            continue
        # get rid of the repetitive output
        try:
            if data["chemical_name"] not in chemical_name:
                chemical_name.add(data["chemical_name"])
                responses.append(data)
            else:
                continue
        except KeyError:
            continue

    return responses
