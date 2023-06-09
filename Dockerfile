FROM python:3.9
WORKDIR /api
ENV PATH /app/node_modules/.bin:$PATH
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api/
EXPOSE 8000
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]