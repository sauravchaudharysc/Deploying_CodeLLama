from django.apps import AppConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import time
import torch
import warnings
import os
import atexit
import signal
import sys

warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")

def cleanup(signum=None, frame=None):
    torch.cuda.empty_cache()
    print("Cleaned up resources.")
    sys.exit(0)

class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'llmpredictor'

    tokenizer = None
    model = None
    device = "cuda:7"
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            start_time = time.time()
            model_directory_path = "/ai_bodhitree/CodeLlama"
            adapter_path = "/ai_bodhitree/llmpredictor/services/models/final_checkpoint"
            
            cls.tokenizer = AutoTokenizer.from_pretrained(model_directory_path)
            cls.tokenizer.pad_token = cls.tokenizer.eos_token
            cls.model = AutoModelForCausalLM.from_pretrained(model_directory_path, torch_dtype=torch.bfloat16, device_map=cls.device).eval()
            cls.tokenizer.padding_side = "right"
            cls.model = PeftModel.from_pretrained(cls.model, adapter_path)
            cls.model.eval()
            end_time = time.time()
            print(f"Saurav Loaded model and tokenizer in {end_time - start_time} seconds")
            cls._initialized = True

    def ready(self):
        if not os.environ.get('RUN_MAIN'):
            self.initialize()

atexit.register(cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

