from src.security import DataMasker


def test_email_hashing_standardization():
    """
    Verifies that the email hashing function strips spaces, forces lowercase,
    and produces identical hashes for identical emails regardless of input style.
    """
    email_1 = "  test.user@RAISIN.com  "
    email_2 = "test.user@raisin.com"

    hash_1 = DataMasker.hash_email(email_1)
    hash_2 = DataMasker.hash_email(email_2)

    # Assert checks if a condition is True. If it's True, the test passes!
    assert hash_1 == hash_2
    assert len(hash_1) == 64


def test_name_obfuscation():
    """
    Verifies that names are correctly masked, keeping only the first initials.
    """
    raw_name = "Johnathan Doe"
    expected_mask = "J*** D***"

    assert DataMasker.obfuscate_name(raw_name) == expected_mask


def test_invalid_email_handling():
    """
    Verifies that empty or invalid non-string inputs don't crash the security module.
    """
    assert DataMasker.hash_email(None) == ""
    assert DataMasker.hash_email(12345) == ""
