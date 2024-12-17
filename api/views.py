from django.shortcuts import render
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, redirect, render
import requests
from rest_framework.response import Response
from .serializers import ScrapedDataSerializer
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import ScrapedData
# from django.core.paginator import Paginator
from rest_framework import status
from django.contrib import messages
from django.db.models import Q

# Create your views here.
@api_view(['POST'])
def scrape_url_post_view(request):
    url = request.data.get('url')
    if not url:
        return Response({ 'status' : False, 'message' : 'error - URL is required' }, status=status.HTTP_400_BAD_REQUEST )
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return Response({'status' : False, 'message' : 'error - failed to Fetch the URL'})
        # response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_title = soup.find('title').get_text(strip=True)
        page_content = ' '.join([str(p) for p in soup.find_all('p')])
        scraped_data, created = ScrapedData.objects.get_or_create(url=url, title=page_title, content=page_content)
        if created:
            return Response({ 'status' : True, 'message' : 'Successfully Scraped and saved in the Database', 'data' : {'url' : scraped_data.url, 'content' : scraped_data.content }}, status=status.HTTP_201_CREATED)
        else:
            return Response({ 'status' : False, 'message' : 'Scraped Data already exists.', 'scraped_data' : ScrapedDataSerializer(scraped_data).data })
    except requests.exceptions.RequestException as e:
        return Response({'status' : False, 'message' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def scrape_view(request):
    scraped_datas = ScrapedData.objects.all().order_by('-ScrapedAt')
    serializer = ScrapedDataSerializer(scraped_datas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def scrape_data_detail_view(request, pk):
    try: 
        scraped_data = ScrapedData.objects.get(pk = pk)
        # scraped_data = get_object_or_404(ScrapedData, pk=pk)
        serializer = ScrapedDataSerializer(scraped_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ScrapedData.DoesNotExist:
        return Response({ 'status' : False, 'error' : 'Scraped Data not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def search_data_view(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'status' : False, 'error' : "Search query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
    scraped_datas = ScrapedData.objects.filter(Q(title__icontains = query) | Q(content__icontains = query))
    if scraped_datas.exists():
        serializer = ScrapedDataSerializer(scraped_datas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({ 'status' : False, 'message' : 'No Scraped Data found for the given query.'}, status=status.HTTP_404_NOT_FOUND)