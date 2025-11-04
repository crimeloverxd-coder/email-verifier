# Email Verifier

A Python application that verifies email addresses using port 25 SMTP verification and detects disposable emails.

## Features

- **Email Format Validation**: Validates email address format using regex
- **SMTP Verification**: Connects to mail server via port 25 to verify email existence
- **Disposable Email Detection**: Identifies temporary/disposable email addresses
- **JSON Response**: Returns structured data with verification results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/crimeloverxd-coder/email-verifier.git
cd email-verifier
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- `dnspython`: For DNS lookups
- `email-validator`: For email format validation
- `disposable-email-domains`: For detecting disposable email providers

## Usage

### Command Line

Run the application:
```bash
python email_verifier.py
```

The application will prompt you to enter an email address for verification.

### Example Output

```json
{
  "email_verified": true,
  "is_disposable": false
}
```

### Response Fields

- `email_verified`: Boolean indicating if the email address is valid and reachable
- `is_disposable`: Boolean indicating if the email is from a disposable/temporary email provider

## How It Works

1. **Format Validation**: Checks if the email follows proper email format
2. **Domain Validation**: Verifies the domain exists and has MX records
3. **SMTP Verification**: Connects to the mail server on port 25 to verify the email exists
4. **Disposable Check**: Compares the domain against a list of known disposable email providers

## Example Usage

```python
from email_verifier import verify_email

# Verify an email
result = verify_email("test@example.com")
print(result)
# Output: {'email_verified': True, 'is_disposable': False}
```

## Technical Details

- Uses port 25 for SMTP verification as required
- Implements proper error handling for network issues
- Includes timeout mechanisms to prevent hanging
- Supports both IPv4 and IPv6 mail servers

## Limitations

- Some mail servers may block SMTP verification attempts
- Requires network access to function properly
- May be rate-limited by some email providers
- Port 25 may be blocked by some ISPs

## Repository

- **GitHub**: [https://github.com/crimeloverxd-coder/email-verifier](https://github.com/crimeloverxd-coder/email-verifier)
- **Author**: crimeloverxd-coder

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
