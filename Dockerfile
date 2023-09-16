FROM python:3.11 as BUILD
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ .

FROM python:3.11-alpine as MAIN
COPY --from=BUILD /opt/venv /opt/venv
COPY app/ /app
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]