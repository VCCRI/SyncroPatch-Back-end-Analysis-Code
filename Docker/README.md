## on windows
```
docker run -it --rm  `
-v 'server-PWD:/SyncroPatch-Back-end-Analysis-Code' `
-v /datadrive:/datadrive `
syncropatch:python `
dummy_raw_data_extraction.py
```

## on linux
```
docker run -it --rm  \
-v 'server-PWD:/SyncroPatch-Back-end-Analysis-Code' \
-v /datadrive:/datadrive \
syncropatch:python \
dummy_raw_data_extraction.py
```

