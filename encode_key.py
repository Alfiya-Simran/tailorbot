import base64

with open("backend/service_account.json", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

print("\n🔐 Paste the following into Render ENV as `SERVICE_ACCOUNT_B64`:\n")
print(encoded)
