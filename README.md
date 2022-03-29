# service_guid

![Python v3.7](https://img.shields.io/badge/Python-3.7-green?style=for-the-badge)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)

Service to generate GUID/token.

Canarie has a PostgreSQL database running. So only need to manually create the table, using the file create_table.sql, and call the service like below.

```python
import requests
server = 'http://server:5001/token12/user2' # /table/key
s = requests.session()
r = s.get(server)
print(r.status_code)
print(r.text)
```
