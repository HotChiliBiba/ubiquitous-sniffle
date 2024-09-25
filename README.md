# cron_job_add.py
    Структура обусловлена рассчетом на последующую доработку для личных нужд e.g добавление флагов с командной строки

# vm_scrape.py
    Collects required data via psutils and sends it to VM by 

# get_data_csv.py
    For some reason the output is inconsistent

## Workaround
    Issue persists, while method of dynnamic calculating of delta time is used. If deltatime is fixed at one hour, issue is resolved

## Probable cause
    1. I failed at properly creating a crontab
    2. VM refuses to add entries, if they contain the same information --- Less probable