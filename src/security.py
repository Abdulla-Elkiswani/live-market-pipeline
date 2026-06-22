import hashlib


class DataMasker:
    """
    A dedicated security class to handle data obfuscation and cryptographic hashing 
    for sensitive customer or candidate PII fields.
    """

    @staticmethod
    def hash_email(email: str) -> str:
        """
        Converts an email address into an irreversible SHA-256 hash.
        If the email is empty or invalid, returns an empty string.
        """
        if not email or not isinstance(email, str):
            return ""

        # Strip spaces and convert to lowercase so that variations in typing
        # (e.g., 'John@DB.com' vs 'john@db.com') produce the exact same hash value.
        clean_email = email.strip().lower()

        # Convert the text string to bytes and apply SHA-256 hashing
        email_bytes = clean_email.encode('utf-8')
        hashed_bytes = hashlib.sha256(email_bytes)

        # Return the readable hexadecimal string version of the hash
        return hashed_bytes.hexdigest()

    @staticmethod
    def obfuscate_name(name: str) -> str:
        """
        Masks a full name by preserving only the first letter of each part 
        and replacing the rest with asterisks (e.g., 'John Doe' -> 'J*** D***').
        """
        if not name or not isinstance(name, str):
            return "ANONYMOUS"

        parts = name.strip().split()
        masked_parts = []

        for part in parts:
            if len(part) > 0:
                # Keep the first letter uppercase and mask the remainder of the word
                masked_parts.append(f"{part[0].upper()}***")

        return " ".join(masked_parts)
