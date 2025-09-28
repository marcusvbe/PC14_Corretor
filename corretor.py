# spell.py
"""
Spell checker simples para português (ortografia).
API principal:
  sc = SpellChecker(corpus_path="corpus_pt.txt")
  sc.correction("errou") -> "errou" ou sugestão
  sc.correct_sentence("Frase com erru") -> (corrected_text, corrections_dict)

Funciona sem dependências externas (puro Python).
"""

import re
from collections import Counter
from pathlib import Path
from typing import Tuple, Dict, List

_LETTERS = "abcdefghijklmnopqrstuvwxyzáàâãéêíóôõúüç"

_WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")


def words(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÀ-ÿ]+", text.lower())


def edit_distance(a: str, b: str) -> int:
    """Distância de Levenshtein (iterativa, O(len(a)*len(b)))."""
    if a == b:
        return 0
    na, nb = len(a), len(b)
    if na == 0:
        return nb
    if nb == 0:
        return na
    prev = list(range(nb + 1))
    cur = [0] * (nb + 1)
    for i in range(1, na + 1):
        cur[0] = i
        ai = a[i - 1]
        for j in range(1, nb + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(prev[j] + 1,          # delete
                         cur[j - 1] + 1,       # insert
                         prev[j - 1] + cost)   # replace
        prev, cur = cur, prev
    return prev[nb]


class Corretor:
    def __init__(self, corpus_path: str = None, min_freq: int = 1):
        """
        corpus_path: arquivo de texto grande (pt-BR) com palavras;.
        min_freq: frequência mínima para considerar palavra válida no vocabulário.
        """
        self.W = Counter()
        if corpus_path:
            p = Path(corpus_path)
            if p.exists():
                txt = p.read_text(encoding="utf-8", errors="ignore")
                self.W = Counter(words(txt))
                
        if min_freq > 1:
            self.W = Counter({w: f for w, f in self.W.items() if f >= min_freq})

        self.N = sum(self.W.values()) or 1

    def P(self, word: str) -> float:
        return self.W[word] / self.N if self.N else 0.0

    def edits1(self, word: str):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + (R[1:] if len(R) > 0 else "") for L, R in splits if R for c in _LETTERS]
        inserts = [L + c + R for L, R in splits for c in _LETTERS]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word: str):
        return {e2 for e1 in self.edits1(word) for e2 in self.edits1(e1)}

    def known(self, words_set):
        return {w for w in words_set if w in self.W}

    def candidates(self, word: str):
        """Retorna conjunto de candidatos plausíveis para 'word'."""
        if word in self.W:
            return {word}
        c1 = self.known(self.edits1(word))
        if c1:
            return c1
        c2 = self.known(self.edits2(word))
        if c2:
            return c2
        closest = self._closest_by_edit_distance(word)
        return {closest} if closest else {word}

    def _closest_by_edit_distance(self, word: str):
        best = None
        best_d = None
        for w in self.W:
            d = edit_distance(word, w)
            if best is None or d < best_d:
                best, best_d = w, d
                if best_d == 0:
                    break
        return best

    def correction(self, word: str) -> str:
        """Corrige UMA palavra (passar em lowercase). Retorna a sugestão (ou a própria palavra)."""
        if not word:
            return word
        low = word.lower()
        cands = self.candidates(low)
        
        # Primeiro priorizar distância
        min_dist = min(edit_distance(low, w) for w in cands)
        closest_cands = [w for w in cands if edit_distance(low, w) == min_dist]
        
        # Depois usar frequência apenas para desempate
        if closest_cands:
            best = max(closest_cands, key=self.P)
        else:
            best = word
            
        return best.capitalize() if word[0].isupper() else best

    def correct_sentence(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Corrige todas palavras em 'text'.
        Retorna (corrected_text, corrections) onde corrections é dict original->sugestao.
        Mantém separadores (pontuação/espacos).
        """
        parts = re.split(r'(\W+)', text, flags=re.UNICODE)
        corrected_parts = []
        corrections = {}
        for p in parts:
            if _WORD_RE.fullmatch(p):
                cand = self.correction(p)
                corrected_parts.append(cand)
                if cand.lower() != p.lower():
                    corrections[p] = cand
            else:
                corrected_parts.append(p)
        return "".join(corrected_parts), corrections


# Remover/comentar este trecho ao final do arquivo
"""
sc = Corretor(corpus_path="vocab.txt")

while True:
    test = input("Entrada: ")
    corrected, changes = sc.correct_sentence(test)
    print("Será que você não quis dizer:", corrected)
    print(changes, "\n")
"""

# Opcional: adicionar este trecho para testes locais
if __name__ == "__main__":
    sc = Corretor(corpus_path="vocab.txt")
    while True:
        test = input("Entrada: ")
        corrected, changes = sc.correct_sentence(test)
        print("Será que você não quis dizer:", corrected)
        print(changes, "\n")
