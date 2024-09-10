import os
from celery import shared_task
from .apps import PredictorConfig
from .services.grading_bt import *

@shared_task(bind=True)
def query_codellama(self, submissions, problem_statement, criterion_info,
                    criterion_name="", max_length=4096, few_shot=False, few_shot_examples=0, train_split=0.7):
    # Ensure the model and tokenizer are initialized
    print("Initiating auto evaluation")
    PredictorConfig.initialize()

    tokenizer = PredictorConfig.tokenizer
    model = PredictorConfig.model
    device = PredictorConfig.device

    if tokenizer is None or model is None:
        raise ValueError("Tokenizer or model not initialized.")
    
    grades = grade_submissions(
        tokenizer=tokenizer, model=model, device=device, problem_statement=problem_statement,
        submissions=submissions, criterion_info=criterion_info, criterion_name=criterion_name,
        max_length=max_length, few_shot=few_shot, few_shot_examples=few_shot_examples, train_split=train_split
    )

    rating_id_map = {}

    for criterion_obj in criterion_info: 
        raw_options = criterion_obj["Ratings"]
        criterion_id = str(criterion_obj["id"])

        rating_id_map[criterion_id] = {}

        for option_obj in raw_options:
            rating_id_map[criterion_id][option_obj["title"]] = option_obj["id"]
    
    combined_json = {}

    for criterion_id, response in grades.items(): 
        llm_ratings = extract_llm_ratings("", "", response)
        for student_id, result in llm_ratings.items(): 
            rating = result[0]
            reasoning = result[1]
            llm_ratings[student_id][0] = rating_id_map[criterion_id][rating]
            llm_ratings[student_id][1] = reasoning 
            
        combined_json[criterion_id] = llm_ratings

    return combined_json

