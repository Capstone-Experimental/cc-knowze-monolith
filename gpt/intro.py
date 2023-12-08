import wikihowunofficialapi as wha

def get_intros(prompt, max_results):
    result = wha.search_wikihow(prompt, max_results, lang='id')
    list_intro = []
    for r in result:
        intro = r.intro
        list_intro.append(intro)
    return list_intro

# print(get_intros("cara memasak bayam", 3))