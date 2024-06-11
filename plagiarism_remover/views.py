from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize NLTK stopwords
stop_words = set(stopwords.words("english"))


def plagiarism_remover(word):
    synonyms = []
    if word in stop_words:
        return word
    if wordnet.synsets(word) == []:
        return word
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    pos_tag_word = nltk.pos_tag([word])
    pos = []
    for syn in synonyms:
        pos.append(nltk.pos_tag([syn]))
    final_synonyms = []
    for pos_syn in pos:
        if pos_tag_word[0][1] == pos_syn[0][1]:
            final_synonyms.append(pos_syn[0][0])
    final_synonyms = list(set(final_synonyms))
    if final_synonyms == []:
        return word
    if word.istitle():
        return random.choice(final_synonyms).title()
    else:
        return random.choice(final_synonyms)


def plagiarism_removal(para):
    para_split = word_tokenize(para)
    final_text = []
    for word in para_split:
        final_text.append(plagiarism_remover(word))
    final_text = " ".join(final_text)
    return final_text


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Add token authentication
@permission_classes([IsAuthenticated])
def plagiarism_removal_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')

        # Preserve line breaks
        paragraphs = text.split('\n')
        modified_paragraphs = []
        for paragraph in paragraphs:
            modified_paragraphs.append(plagiarism_removal(paragraph))

        return JsonResponse({'paragraphs': modified_paragraphs})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'})
