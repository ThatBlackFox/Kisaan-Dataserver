# Kisaan Proxy

> This is a small fast api server which will simulate data acquisition of crop prices on a daily basis.

## Setup
### For windows:

```shell
python -m venv kisaan
.\kisaan\Scripts\Activate.ps1
pip install -r requirement.txt
fastapi dev .\proxy.py
```
### For linux:
```bash
python -m venv kisaan
source kisaan/bin/activate
pip install -r requirement.txt
fastapi dev .\proxy.py
```

## Starting the server:
```
fastapi dev .\proxy.py
```

## Accessing the docs:
```
 http://127.0.0.1:8000/docs
```
## FAQs

there are no faqs just talk to me