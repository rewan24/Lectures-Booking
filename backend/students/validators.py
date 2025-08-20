import re
from rest_framework import serializers

EG_PHONE_REGEX = re.compile(r"^01[0-2,5][0-9]{8}$")  
def validate_egypt_phone(value: str) -> str:
    v = value.strip().replace(" ", "")
    if v.startswith("+2"):
        v = v[2:]
    if not EG_PHONE_REGEX.match(v):
        raise serializers.ValidationError("رقم الهاتف المصري غير صالح. مثال: 01012345678")
    return v
