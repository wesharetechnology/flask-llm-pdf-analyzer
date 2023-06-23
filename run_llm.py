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
    responses = {"chemical_info": []}
    chemical_name = set()
    # put the pdf text in a string
    i = 0
    for sentence in sentences:
        # feed each sentence to the model
        prompt = """Extract "chemical_name" (keyword,content) from the text above, 
                    also content such as "chemical_property", "chemical_hazard" and output in json format.
                    Do not output anything if there is no chemical name.
                    Skip the citation and reference.
                    Output JSON object only."""
        i += 1
        llm_input = "{}\n\n{}".format(sentence, prompt)
        response, history = model.chat(tokenizer, llm_input, history=[])
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
                responses["chemical_info"].append(data)
            else:
                continue
        except KeyError:
            continue
        if i > 10:
            break
    return responses
