import requests
from bs4 import BeautifulSoup
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        # Check if the file is uploaded
        if not file:
            return Response({"error": "No file uploaded."}, status=400)

        # Check if the file type is valid
        if not file.name.endswith('.txt'):
            return Response({"error": "Invalid file type. Please upload a .txt file."}, status=400)

        try:
            # Read and decode the file
            urls = file.read().decode('utf-8').splitlines()
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=500)

        scraped_data = []

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Clean the text by replacing multiple newlines with a single space
                content = ' '.join(soup.get_text().split())
                scraped_data.append({
                    'url': url,
                    'content': content
                })
            except requests.exceptions.HTTPError as http_err:
                scraped_data.append({
                    'url': url,
                    'error': f"HTTP error occurred: {str(http_err)}"
                })

            except requests.exceptions.RequestException as req_err:
                '''requests.exceptions.RequestException: This is a base class for all exceptions raised by the 
                                requests library. It can cover a variety of issues that may occur when making a request, 
                                such as network problems, invalid URLs, or timeouts.'''
                scraped_data.append({
                    'url': url,
                    'error': f"Request error occurred: {str(req_err)}"
                })
            except Exception as e:
                scraped_data.append({
                    'url': url,
                    'error': f"An error occurred: {str(e)}"
                })

        return Response(scraped_data, status=200)
