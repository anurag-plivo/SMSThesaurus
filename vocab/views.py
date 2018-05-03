# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from vocabulary.vocabulary import Vocabulary as vb

import json
import random

# Create your views here.

class VocabularyAPIView(APIView):

    def randomizer(self):
        res = [True, False]
        return res[random.randint(0, 1)]

    def addLine(self):
        return "\n"

    def more(self, values):
        res = ''
        for val in values:
            if self.randomizer():
                res += ', '
                res += val
        return res

    def statement(self, sentence):
        sentence = ''.join(sentence.strip().split(';'))
        sentence = sentence.split('&quot')
        if len(sentence)>1:
            sentence = sentence[0].strip() + '. For e.g., ' + sentence[1].strip() + '.'
        else:
            sentence = sentence[0]
        return sentence

    def meaning(self, word):
        definition = 'DEFINITION: '
        word_meaning = vb.meaning(word, format="list")
        if not word_meaning:
            return False
        definition += vb.meaning(word, format="list")[0]
        definition = self.statement(definition)
        definition += self.addLine()
        return definition

    def synonym(self, word):
        res = 'SYNONYMS: '
        synonyms = vb.synonym(word, format="list")
        if not synonyms:
            return False
        res += synonyms[0]
        res += self.more(synonyms[1:])
        res += self.addLine()
        return res

    def antonym(self, word):
        res = 'ANTONYMS: '
        antonyms = vb.antonym(word, format="list")
        if not antonyms:
            return False
        res += antonyms[0]
        res += self.more(antonyms[1:])
        res += self.addLine()
        return res

    def get(self, request, *args, **kwargs):
        text = request.GET.get('text', '')
        data = ''
        word_meaning = self.meaning(text)
        word_synonym = self.synonym(text)
        word_antonym = self.antonym(text)
        if not word_meaning:
            return Response(data="Word not found", status=status.HTTP_404_NOT_FOUND)
        data += word_meaning
        if word_synonym:
            data += word_synonym
        if word_antonym:
            data += word_antonym
        return Response(data=data, status=status.HTTP_200_OK)



Vocabulary = VocabularyAPIView.as_view()