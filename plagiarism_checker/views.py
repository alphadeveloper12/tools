from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from django.utils.html import mark_safe
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
class PlagiarismCheckView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        text_to_check = request.data.get('text')
        className = request.data.get('className')

        burp0_url = "https://papersowl.com:443/plagiarism-checker-send-data"
        burp0_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://papersowl.com/free-plagiarism-checker",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://papersowl.com",
            "Dnt": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Te": "trailers",
            "Connection": "close"
        }
        burp0_cookies = {
            "PHPSESSID": "qjc72e3vvacbtn4jd1af1k5qn1",
            # Include other cookies here as per your requirement
        }
        burp0_data = {
            "is_free": "false",
            "plagchecker_locale": "en",
            "product_paper_type": "1",
            "title": '',
            "text": str(text_to_check)
        }

        # Make the request
        r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

        result = json.loads(r.text)

        # Extract the match with the highest percentage
        highest_match = max(result["matches"], key=lambda x: float(x["percent"]))

        # Get the original text and initialize a list to hold highlighted sections
        original_text = text_to_check
        highlighted_sections = []

        # Wrap plagiarized sections in HTML span tags and collect indexes
        for start, end in highest_match["highlight"]:
            start_idx = int(start)
            end_idx = int(end)
            matched_text = text_to_check[start_idx:end_idx]
            original_text = original_text[:start_idx] + \
                f'<span class="{className}">{matched_text}</span>' + \
                original_text[end_idx:]
            highlighted_sections.append({
                "start_index": start_idx,
                "end_index": end_idx,
                "text": matched_text
            })

        response_data = {
            "text_with_highlights": mark_safe(original_text),  # Mark as safe to render HTML
            "percentage": highest_match["percent"],
            "url": highest_match["url"],
            "highlighted_sections": highlighted_sections
        }

        return Response(response_data, status=status.HTTP_200_OK)



