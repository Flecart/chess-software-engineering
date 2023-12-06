import requests
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)
   # This is the base instruction to our model to tell him examples of what he needs to say
    # to entartain the audience
    # Examples are Chain-of-Thought format prompting
    # Adapted from : https://github.com/zq99/banter_blitz_transcript_merge
BASE_STRING = """
You are a chess commentator interested to entartain the audience.
You will be given a FEN state, a move and you need to say something funny about it.
Here are examples of what commentators say:
if knight c6 maybe I'll go Knight d2 if
he takes King d2 - I think my King is
more or less fine in the center and if
Knight g3 hg at least I got a normal
position
yeah bishop d3 probably takes on d2 - I'm
gonna do that anyway
the thing is if he if he went like
Knight d2 King d2 - I would have gone
Bishop e2 - and if he had would have gone Knight g3
hg c6 then I would probably I wanted to
trade the bishops the difference being something about the
dark squares no sorry the light squares
on the on the kingside with with the h
file opened compared to to this where my
King is in the center now I think I'm
doing fine I'm intending h4 pretty soon
and my King is perfectly safe
he goes for f5 but seems bit overzealous
to me I go h4 he goes g4 maybe I
don't achieve that much so I could go g4 as
well no reason to be scared f4 as well
think I'm gonna go h4
and my queen is protecting my king very
well so this move I don't like for him now
I get Bishop e5 with tempo
I'm going h4 next oh and I just
missed this okay
yeah that's why I never
Rook e5 then knight e5 because then my
queen would have been kicked away at the
very least so I can go rook h1
yeah I probably don't have a whole lot
hear still so okay let me just go b3
protect my stuff Queen f4
probably a very good move which I completely
missed
I can not go Rook g4 because queen g4
that's the that's the main issue here I
can't go queen d4 no I can't go Queen
d4 maybe I have Queen f5 actually
ah, he takes that rook.

Here is the end of the comment. Please be concise and funny in your version.
"""

def query_hf(prompt, engine="gpt2", temperature=1, max_tokens=50):
    """queries Hugginface API for a prompt and returns the generated text.
    """
    raise ValueError("This function is deprecated (not good performance), use chat() instead")
    query ={"inputs": BASE_STRING + "Write a comment for: " + prompt,
            "parameters": {
                "temperature": temperature,
                "do_sample": False,
                "max_new_tokens": max_tokens, 
                "max_time": 120
            },
            "options":{"wait_for_model":True}
    }

    endpoint_url = "https://api-inference.huggingface.co/models/" + engine
    headers = {"Authorization": "Bearer "+ ""} # HUGGINGFACE_API_KEY}
    response = requests.post(endpoint_url, headers=headers, json=query, timeout=120)
    out = response.json()
    out = out[0]["generated_text"][len(prompt):]

    return out

def chat(msgs, model="gpt-3.5-turbo", temperature=1, max_tokens=50, **kwargs):
    """ Function for quering ChatGPT models
    """
    if str(type(msgs))=="<class 'str'>":
        print("INPUT: "+msgs)
        msgs=[{"role": "system", "content": BASE_STRING},
              {"role": "user", "content": "Write a comment for: " + msgs}]
    else:
        print("INPUT: " + msgs[len(msgs) - 1]["content"])

    out = client.chat.completions.create(**kwargs, model=model, messages=msgs, max_tokens=max_tokens, temperature=temperature)
    content = out.choices[0].message.content

    # TODO:
    # We should return the whole conversation, because GPT is optimized for it,
    # for soimplicity we just return the last message
    # msgs.append({"role": "assistant", "content": content})
    return content

def __test_beginning_gpt():
    msgs = chat("FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR, move: e2e4")
    print(msgs)

def __test_huggingface():
    print(query_hf("FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR, move: e2e4", engine="alpindale/goliath-120b"))

def __test_middle():
    msgs = chat("FEN: r5k1/5ppp/1p6/p1p5/7b/1PPrqPP1/1PQ4P/R4R1K b - - 0 1, move: h4g3")
    print(msgs)

if __name__ == "__main__":
    __test_middle()