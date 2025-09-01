# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
### Added
- Placeholder for upcoming features (e.g., SMTP checks, OAuth2 support, 1Password CLI integration).

---

## [v1.0.0] - 2025-09-01
### Added
- Initial release of the **IMAP Password Checker**.
- Support for verifying IMAP credentials with SSL (993), STARTTLS (143), and Plain (143).
- Single account checks and batch checks via `accounts.csv`.
- Secure password input (hidden, not stored).
- Example `accounts.csv.example` file for safe configuration.
- `README.md` with instructions and usage examples.
- `.gitignore` excluding sensitive files like `accounts.csv`.

### Fixed
- Removed `accounts.csv` from Git tracking to protect sensitive information.

### Known Issues
- Gmail, iCloud, Yahoo: require **App Passwords** if 2FA is enabled.
- Office365/Exchange Online: may not allow Basic Auth; OAuth2 support not yet available.
- Only IMAP tested — SMTP checks not included in this release.

---

[Unreleased]: https://github.com/rcaservices/check_imap_passwords/compare/v1.0.0...HEAD
[v1.0.0]: https://github.com/rcaservices/check_imap_passwords/releases/tag/v1.0.0
