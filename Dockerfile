FROM nikolaik/python-nodejs:python3.12-nodejs20 AS builder

WORKDIR /frontend
COPY frontend/package*.json .
RUN npm ci
COPY ./frontend .
RUN npm run build
RUN npm prune --production


FROM nikolaik/python-nodejs:python3.12-nodejs20

WORKDIR /app
COPY app/ /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

WORKDIR /frontend
COPY --from=builder /frontend/build build/
COPY --from=builder /frontend/node_modules node_modules/
COPY frontend/package.json .
COPY frontend/.env .
ENV NODE_ENV=production

EXPOSE 3000
EXPOSE 8080

COPY .docker-start.sh /start.sh
RUN  chmod +x /start.sh

CMD /start.sh
