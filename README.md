# applooma (Python)

```bash
pip install applooma
```

```python
from applooma import AppServerClient

applooma = AppServerClient(api_key="...", api_secret="...")
res = applooma.create_token(room_name="room1", identity="user1", role="host")
# res["token"], res["wsUrl"]
```
Docs: https://applooma.dev/dashboard/docs
