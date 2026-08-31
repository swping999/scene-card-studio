# Security Policy

Scene Card Studio processes local photographs, file paths, metadata, manifests, generated images, and optional cloud-upload consent. Reports that show unintended disclosure, unauthorized file access, integrity bypass, or unsafe execution are especially valuable.

## Supported versions

Security fixes are applied to the latest release and the `main` branch. Older releases may be used to reproduce a report but are not maintained separately.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository:

<https://github.com/swping999/scene-card-studio/security/advisories/new>

Do not open a public issue for a vulnerability before the maintainer has had a reasonable opportunity to investigate it. Include:

- affected version or commit;
- operating system and Python version;
- the entry point and required attacker control;
- a minimal reproduction using non-sensitive sample files;
- expected and observed behavior;
- the potential effect on confidentiality, integrity, or availability.

You should receive an acknowledgement within seven days. Validation and remediation timelines depend on severity and reproducibility.

## In-scope security properties

- Source photos remain local unless the user explicitly approves the provider, purpose, and exact upload list.
- User-controlled paths cannot read, overwrite, or embed unintended local files.
- Embedded raster images are decoded, bounded, stripped of metadata, and safely re-encoded.
- Prompt, Render, Retry, and Review Manifests cannot substitute unbound outputs or bypass required hashes and output contracts.
- Captions, filenames, metadata, Scene Cards, and manifests cannot inject executable commands or unsafe SVG markup.
- The core package does not silently execute shell commands, transmit credentials, or make undeclared network requests.
- Repository history and release artifacts do not expose credentials, private photographs, or personal cloud-consent records.

## Out of scope

- The behavior, availability, retention policy, or model output of a third-party image-generation provider after the user has explicitly approved an upload.
- Purely aesthetic disagreements without a security or privacy impact.
- Denial of service requiring the reporter to exhaust their own local machine without crossing a trust boundary.

Please use only fictional or self-owned test images. Do not include another person's private photographs or live credentials in a report.
