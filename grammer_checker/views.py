# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from happytransformer import HappyTextToText, TTSettings
import difflib
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Add token authentication
@permission_classes([IsAuthenticated])
def grammar_correction(request):
    if request.method == 'POST':
        # Get the input text from the request data
        input_text = request.data.get('input_text', '')

        # Initialize HappyTextToText model
        happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

        # Set model settings
        args = TTSettings(num_beams=5, min_length=1)

        # Generate corrected text
        result = happy_tt.generate_text("grammar: " + input_text, args=args)

        # Highlight changed parts
        highlighted_text = highlight_corrected_parts(input_text, result.text)

        # Return the highlighted corrected text in the response
        return Response({'corrected_text': highlighted_text})

def highlight_corrected_parts(original_text, corrected_text):
    # Use difflib to find the differences between the original and corrected text
    diff = difflib.ndiff(original_text.split(), corrected_text.split())

    # Create a list to store the highlighted parts
    highlighted_parts = []

    for item in diff:
        if item.startswith('+'):
            # Add the corrected part with highlighting
            highlighted_parts.append('<span class="corrected">{}</span>'.format(item[2:]))
        else:
            # Add the unchanged part
            highlighted_parts.append(item[2:])

    # Join the parts back into a single string
    highlighted_text = ' '.join(highlighted_parts)

    return highlighted_text
