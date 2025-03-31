from rest_framework import serializers
from .models import Company
from dataclasses import dataclass


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


@dataclass
class Rule:
    input: str
    feature_name: str
    operation: dict
    match: int
    default: int


class RuleSerializer(serializers.Serializer):
    input = serializers.CharField(max_length=255)
    feature_name = serializers.CharField(max_length=255)
    operation = serializers.DictField()
    match = serializers.IntegerField()
    default = serializers.IntegerField()

    def create(self, validated_data):
        return Rule(**validated_data)
