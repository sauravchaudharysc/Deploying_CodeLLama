# In llmpredictor/views.py
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import json
import time
from .serializers import FileUploadSerializer
import zipfile
from .tasks import query_codellama
from .services.dataset_utils import extract_llm_ratings

def home(request):
    return HttpResponse("Welcome to Auto Grading Server")

class Predictor(APIView):
    def post(self, request):
        start_time = time.time()
        if request.method == 'POST':
            print(f"I am the original {request}")
            data = request.data
            print(f"I am the original data {data}")
            # save the submissions
            submissions = {}
            print(f"the request files are {request.FILES}")
            for key, file_list in request.FILES.lists():
                # Read the content of the file (assuming each key has a single file)
                file_content = file_list[0].read().strip()
                submissions[key] = file_content
            print(f"submission dictonary {submissions}\n\n")

            # Save problem statement
            ps = data['problem_statement']

            # Save criteria
            criteria_json = request.data.get('criteria')
            criteria = json.loads(criteria_json)
    
            print(f"the criteria {criteria}\n")

            try:
                print("calling asyncrounous task\n")
                task = query_codellama.apply_async(
                    args=[submissions, ps, criteria],
                    kwargs={
                            'criterion_name': "",
                            'max_length': 4096, 
                            'few_shot': False, 
                            'few_shot_examples': 0, 
                            'train_split': 0.7
                            }
                        )
                
                '''
                #For Asynchronous
                task = query_codellama(
                    submissions, ps, criteria)'''
                    
                end_time = time.time()
                print("Done Everything :", end_time - start_time)
                return Response({'status code': 202, 'task': task.id}, status=202)
            except Exception as e:
                print(e)
                end_time = time.time()
                print("Total time taken :", end_time - start_time)
                return Response(status=404, data={'status': 404, 'message': 'Something went wrong'})

    def get(self, request):
        start_time = time.time()
        task_id = request.data['task_id']
        task_result = AsyncResult(task_id)
        print(task_result)
        if task_result.status == "SUCCESS":
            print(task_result.result)
            end_time = time.time()
            print("Total time taken :", end_time - start_time)
            return Response(task_result.result, status=200)
        else:
            end_time = time.time()
            print("Total time taken :", end_time - start_time)
            return Response({"message": "task pending"}, status=202)
