from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import enum
import os
import re
import string

import fasttext
import fasttext.util
import numpy as np
import torch
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

EMBEDDINGS_FILE = 'embeddings.pt'
PHRASES_FILE = 'phrases.pt'

stop_words = set(stopwords.words('english'))
stop = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
cos = torch.nn.CosineSimilarity(dim=0)
fasttext_model = None


def get_embedding(s):
    return get_fasttext_embedding(s)


def get_fasttext_embedding(q):
    global fasttext_model
    q = preprocess_single_str(q)
    if fasttext_model is None:
        command_download("en", if_exists='ignore')
        fasttext_model = fasttext.load_model("cc.en.300.bin")
    return torch.Tensor(fasttext_model.get_sentence_vector(q))


def command_download(lang_id, if_exists):
    """
        Download pre-trained common-crawl vectors from fastText's website
        https://fasttext.cc/docs/en/crawl-vectors.html
    """
    fasttext.util.download_model(lang_id, if_exists)


def preprocess_single_str(s):
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = re.sub(r'[0-9]+', '', s)
    s = word_tokenize(s)
    s = [word.lower() for word in s]
    s = [word for word in s if word not in (stop)]
    s = [lemmatizer.lemmatize(word) for word in s]
    s = ' '.join(s)
    return s


def cosine_similarity(q1, q2):
    return cos(q1.reshape(-1), q2.reshape(-1)).item()


def create_and_save_phrase_embeddings(phrases, emb_path=EMBEDDINGS_FILE, phrases_path=PHRASES_FILE):
    embeddings = torch.zeros((len(phrases), 300))
    for ind, phrase in enumerate(phrases):
        embeddings[ind] = get_embedding(phrase)
    torch.save(embeddings, emb_path)
    np.savetxt(phrases_path, np.array(phrases), fmt="%s")
    return embeddings


def load_embeddings(path=EMBEDDINGS_FILE):
    if not os.path.isfile(path):
        return None
    return torch.load(path)


def load_phrases(path=PHRASES_FILE):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        phrases = [line.rstrip('\n') for line in f]
        return phrases


def get_most_similar(s, embeddings=None, phrases=None):
    if embeddings is None:
        embeddings = load_embeddings()
        if embeddings is None:
            return None

    if phrases is None:
        phrases = load_phrases()
        if phrases is None:
            return None

    s_emb = get_embedding(s)
    best_score = None
    best_phrase = None

    for ind in range(embeddings.shape[0]):
        cos_sim = cosine_similarity(embeddings[ind], s_emb)
        if best_score is None or best_score < cos_sim:
            best_score = cos_sim
            best_phrase = phrases[ind]

    return best_phrase, best_score


def get_scenario_list(scenario):
    result = []
    for s in scenario:
        for ind, p in enumerate(s['prompts']):
            result.append((s['id'], p, s['type'], get_embedding(p), ind))
    return result


def process_agreement(s):
    AGREEMENT_EMB_PATH = 'agreement_emb.pt'
    AGREEMENT_PHRASES_PATH = 'agreement_phrases.pt'
    agreement_phrases = ['yes', 'no']

    emb = None
    if not os.path.isfile(AGREEMENT_EMB_PATH):
        emb = create_and_save_phrase_embeddings(agreement_phrases,
                                                emb_path=AGREEMENT_EMB_PATH,
                                                phrases_path=AGREEMENT_PHRASES_PATH)
    else:
        emb = load_embeddings(path=AGREEMENT_EMB_PATH)
    if emb is None:
        raise ValueError("Failed to load agreement embeddings")

    best_phrase = get_most_similar(
        s, embeddings=emb, phrases=agreement_phrases)
    return best_phrase[0] == 'yes'


def get_input():
    s = input()
    emb = get_embedding(s)
    return s, emb


def find_scenario_record(scenario, id):
    for s in scenario:
        if 'id' in s and s['id'] == id:
            return s
    return None


def get_scenario_record(scenario_prompts, needed_type, inp_emb, certain_id=None):
    best_score = None
    best_match = None

    for p in scenario_prompts:
        id, _, type, emb, _ = p
        if (type != needed_type):
            continue
        if not (certain_id is None) and id != certain_id:
            continue
        cos_sim = cosine_similarity(inp_emb, emb)
        if best_score is None or best_score < cos_sim:
            best_score = cos_sim
            best_match = p

    return best_match


class ChatState(enum.Enum):
    INITIAL = 1
    CHOOSE = 2
