FROM python:3.6-onbuild

# Install essential packages
RUN pip install --upgrade pip && \
    pip3 install sanic

# package for autocorrection
RUN pip3 install requests && \
    pip3 install symspellpy

# package for notify me
RUN pip3 install pandas && \
    pip3 install schedule

# package for autocomplete
RUN pip3 install fast-autocomplete[levenshtein]
