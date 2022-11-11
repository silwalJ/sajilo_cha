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

"""check multiple user login attempts"""


def check_user_login_attempt(user):
    user_attempt = UserLoginAttempt.objects.filter(user=user).first()
    number_time = DynamicLoginAttempt.objects.get(id=1)
    if user_attempt:
        # it checks if the user login attempt is greater than specified number of attempts
        # Minus one have been done to block the user if attempt is 0
        if user_attempt.login_attempts >= number_time.number_of_login_attempt - 1:
            user_attempt.is_locked = True
            user_attempt.save()
            raise serializers.ValidationError(
                {
                    "status": "fail",
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "message": "Your account is blocked, Contact admin",
                }
            )

        else:
            # replacing time zone
            now = datetime.now().replace(tzinfo=pytz.utc)
            user_login_attempt = user_attempt.first_login_attempt

            # subtracting first login with current time
            time = now - user_login_attempt

            # checking if time time is within the 10 minutes
            if timedelta(minutes=number_time.time) < time:

                user_attempt.login_attempts = 1
                user_attempt.first_login_attempt = datetime.now()
                user_attempt.latest_login = datetime.now()
                user_attempt.save()
                raise serializers.ValidationError(
                    {
                        "status": "fail",
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "message": "Login attempt reset",
                    }
                )
            else:

                user_attempt.login_attempts += 1
                user_attempt.save()
                raise serializers.ValidationError(
                    {
                        "status": "fail",
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "message": "Warning! your login attempt is {} and you have {} attempt left!".format(
                            user_attempt.login_attempts,
                            number_time.number_of_login_attempt
                            - user_attempt.login_attempts,
                        ),
                    }
                )
    else:

        UserLoginAttempt.objects.create(
            user=user,
            first_login_attempt=datetime.now(),
            latest_login=datetime.now(),
            login_attempts=1,
        )
