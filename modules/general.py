from PyDictionary import PyDictionary

async def define(word):
    ret = ""
    defs = PyDictionary.meaning(word)
    if defs is not None:
        ret += f"Definitions of **{word}**:\n\n"
        for type in defs:
            ret += f"*{type}*: \n"
            for i, definition in enumerate(defs[type]):
                ret += f"   {i+1}. `{definition}`\n"
            ret += "\n"
    else:
        ret = f"The word `{word}` does not exist!"
    return ret

async def synonyms(word):
    ret = ""
    syns = PyDictionary.synonym(word)
    if syns is not None:
        ret = f"Synonyms of **{word}**:\n\n"
        ret += f"`{', '.join(syns)}"[0:2028-len(word)]+"`"
    else:
        ret = "There are no synonyms for that word!"
    return ret