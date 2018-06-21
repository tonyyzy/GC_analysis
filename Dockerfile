FROM python:3.6.3

WORKDIR /GC_analysis

COPY /scripts/GC_analysis.py /GC_analysis

COPY /requirements.txt /GC_analysis

RUN pip3 install -r requirements.txt

RUN cp GC_analysis.py GC_analysis

ENV PATH "/GC_analysis:$PATH"
