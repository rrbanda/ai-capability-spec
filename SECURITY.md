# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
responsibly.

**Do NOT open a public GitHub Issue for security vulnerabilities.**

Instead, please email the maintainers directly. Contact information is
available in GOVERNANCE.md.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours of receiving the report.
- **Assessment**: Within 1 week, we will assess the severity and impact.
- **Fix**: We aim to release a fix within 2 weeks of confirming a vulnerability.
- **Disclosure**: We will coordinate disclosure timing with the reporter.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.x.x   | Yes       |

## Security Considerations for Providers

Since this is a specification project (not a runtime), security considerations
primarily apply to provider implementations:

- **Credential handling**: Providers implementing the Storage capability (6)
  must handle credentials securely. The spec's Connection model marks
  credential fields as sensitive.
- **Authentication**: The spec does not prescribe authentication mechanisms.
  Providers should implement authentication appropriate to their platform.
- **Authorization**: Workspace-scoped operations should enforce access control
  at the provider level.
- **Input validation**: Providers must validate all inputs against the spec's
  schemas before processing.
