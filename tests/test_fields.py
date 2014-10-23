from django.test import TestCase
from django.test.utils import override_settings

from pgcrypto_fields import fields


PUBLIC_PGP_KEY = 'my public key'


class TestEncryptedTextField(TestCase):
    """Test `EncryptedTextField` behave properly."""
    field = fields.EncryptedTextField

    def test_db_type(self):
        """Check db_type is `bytea`."""
        self.assertEqual(self.field().db_type(), 'bytea')

    @override_settings(PUBLIC_PGP_KEY=PUBLIC_PGP_KEY)
    def test_get_placeholder(self):
        """Check `get_placeholder` returns the right string function to encrypt data."""
        expected = "pgp_pub_encrypt(%s, dearmor('{}'))".format(PUBLIC_PGP_KEY)
        self.assertEqual(self.field().get_placeholder(), expected)

    def test_south_field_triple(self):
        """Check return a suitable description for south migration."""
        south_triple = fields.EncryptedTextField().south_field_triple()
        expected = ('pgcrypto_fields.fields.EncryptedTextField', [], {})
        self.assertEqual(south_triple, expected)
