## What is it for?

 - updates currency rates ones a day according to Central Bank of Russia
 - show all currency rates via `/rates` command
 - converts one currency to another via `/exchange` command
    - converts to rubles `/exchange USD`
    - converts to given currency `/exchange USD EUR`
    - converts with given amount `/exchange USD EUR 100`

## How to deploy

##### It's as simple as
 - `git clone`
 - `cp .env.example .env`
 - adjust envs (bot token at least)
 - `docker compose up`
