# pfsense-backup
Backup Pfsense XML Config

### Quickstart

``` shell
    docker run -it -e pfsense_username="YOUR-USERNAME" \
    -e pfsense_password="YOUR-PASSWORPD" \
    -e pfsense_url="https://xxxx.xxx.xxx/" \
    -v SOME-PLACE:/tmp/ \
    cytram/pfsense-backup
```