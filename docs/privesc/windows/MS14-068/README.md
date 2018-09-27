# Executive Summary


This security update resolves a privately reported vulnerability in Microsoft Windows Kerberos KDC that could allow an attacker to elevate unprivileged domain user account privileges to those of the domain administrator account. An attacker could use these elevated privileges to compromise any computer in the domain, including domain controllers. An attacker must have valid domain credentials to exploit this vulnerability. The affected component is available remotely to users who
have standard user accounts with domain credentials; this is not the case for users with local account credentials only. When this security bulletin was issued, Microsoft was aware of limited, targeted attacks that attempt to exploit this vulnerability.

This security update is rated Critical for all supported editions of Windows Server 2003, Windows Server 2008, Windows Server 2008 R2, Windows Server 2012, and Windows Server 2012 R2. The update is also being provided on a defense-in-depth basis for all supported editions of Windows Vista, Windows 7, Windows 8, and Windows 8.1. For more information, see the Affected Software section.

The security update addresses the vulnerability by correcting signature verification behavior in Windows implementations of Kerberos. For more information about the vulnerability, see the Frequently Asked Questions (FAQ) subsection for the specific vulnerability.

For more information about this update, see Microsoft Knowledge Base Article 3011780.

## Reference for exploitation

https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2014/ms14-068
http://blog.liatsisfotis.com/knock-and-pass-kerberos-exploitation.html

