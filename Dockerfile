FROM library/alpine

WORKDIR /GC_analysis

COPY /dist/GC_analysis /GC_analysis

RUN chmod 777 GC_analysis

ENV PATH "/GC_analysis:$PATH"
