from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    number = serializers.CharField()
    name = serializers.CharField()
    month = serializers.CharField()
    year = serializers.CharField()
    code = serializers.CharField()

    def validate_number(self, value):
        if len(value) < 16:
            raise serializers.ValidationError(
                "Card number should be at least 16 characters long."
            )
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain only numbers.")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Name should be at least 2 characters long."
            )
        if value.isdigit():
            raise serializers.ValidationError("Name must contain only letters.")
        return value

    def validate_month(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Month must contain only numbers.")
        return value

    def validate_year(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Year must contain only numbers.")
        return value

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Code must contain only numbers.")
        if len(value) != 3:
            raise serializers.ValidationError("Code length should be 3")
        return value
