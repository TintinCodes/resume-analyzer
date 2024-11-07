FROM python:3.11.9-slim-bullseye as build
RUN apt-get update -y \
    && apt upgrade -y \
    && apt-get install build-essential -y \
    && apt-get clean \
    && useradd app -d /home/app \ 
    && usermod -aG root app \
    && mkdir -p /home/app/logs  \
    && chown -R app:root /home/app \
    && chmod -R g=u /home/app
ENV HOME=/home/app
ENV PATH="/home/app/.local/bin:${PATH}"
USER app
WORKDIR /home/app
COPY --chown=app:root requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --user -r requirements.txt
COPY --chown=app:root . .
RUN chmod -R g=u /home/app

# Production
FROM python:3.11.9-slim-bullseye
RUN apt-get update -y \
    && apt upgrade -y \
    && apt-get install procps curl jq -y \
    && apt-get clean \
    && useradd app -d /home/app \ 
    && usermod -aG root app \
    && mkdir -p /home/app \
    && chown -R app:root /home/app \
    && chmod -R g=u /home/app
ENV HOME=/home/app
ENV PATH="/home/app/.local/bin:${PATH}"
USER app
COPY --chown=app:root --from=build /home/app /home/app
WORKDIR /home/app/
EXPOSE 8501
CMD streamlit run app.py