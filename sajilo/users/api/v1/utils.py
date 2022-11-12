from rest_framework import serializers


class Util:
    def check_data(self, data, dynamic_fields):
        valid_field_list = []
        mandatory_field_list = []
        non_mandatory_field_list = []
        for mandatory_field in data:
            # print(mandatory_field)
            mandatory_field_list.append(mandatory_field)
        # print(mandatory_field_list)
        for field in dynamic_fields:
            valid_field_list.append(field["fieldname"])
        # print(valid_field_list)
        all_field_list = list(self._kwargs["data"].keys())
        for field in all_field_list:
            if field not in mandatory_field_list:
                non_mandatory_field_list.append(field)
        valid_field_list.sort()
        non_mandatory_field_list.sort()
        # print(valid_field_list)
        # print(non_mandatory_field_list)

        keys = self._kwargs["data"]
        for data in self._kwargs["data"]:
            if keys[data] == "":
                raise serializers.ValidationError(
                    {"data_error": "There are no data in fields"}
                )
        if not valid_field_list == non_mandatory_field_list:
            raise serializers.ValidationError(
                {"value_error": "Upproved unsent/Unapproved sent"}
            )
