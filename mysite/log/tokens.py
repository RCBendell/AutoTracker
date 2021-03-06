# accounts/tokens.
# Chris Bendell ; 10 April 2019

# Not sure this is necessary in the long run
# Creates a unique token in order to activate user
# But I dont think I ended up using it at all

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) #+
            #text_type(user.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
