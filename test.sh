#!/bin/bash

curl -v 'https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=2020&year-to=2020&make=Alfa%20Romeo&model=Giulia&auction-type=All&page=2' \
  -H 'authority: bid.cars' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'pragma: no-cache' \
  -H 'referer: https://bid.cars/en/search/results?search-type=filters&type=Automobile&year-from=2020&year-to=2020&make=Alfa%20Romeo&model=Giulia&auction-type=All' \
  -H 'sec-ch-ua: "Chromium";v="115", "Not/A)Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' \
  --compressed