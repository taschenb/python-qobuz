# python-qobuz

Unofficial python library for the [Qobuz-API](https://github.com/Qobuz/api-documentation).

## Installation

To install, run
```bash
pip install qobuz
```

## Usage
In order to use the library, your application needs a valid APP_ID.
For streaming audio, you also need a valid APP_SECRET.
Both id and secret can be requested from [api@qobuz.com](mailto:api@qobuz.com).

```python
import qobuz

# Register your APP_ID
qobuz.register_app("YOUR_APP_ID")

# Or register your APP_ID and APP_SECRET
qobuz.register_app("YOUR_APP_ID", "YOUR_APP_SECRET")
```
