FROM library/python:3.7-alpine3.7

WORKDIR /GC_analysis

COPY /GC_analysis/GC_analysis.py /GC_analysis

COPY /requirements.txt /GC_analysis

RUN pip3 install -r requirements.txt

RUN mv GC_analysis.py GC_analysis

RUN chmod +777 GC_analysis

ENV PATH "/GC_analysis:$PATH"
