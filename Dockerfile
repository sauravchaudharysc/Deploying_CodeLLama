FROM nvcr.io/nvidia/pytorch:22.05-py3

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN python -m spacy download en_core_web_sm

RUN mkdir /ai_bodhitree
COPY ./ai_bodhitree /ai_bodhitree
WORKDIR /ai_bodhitree
