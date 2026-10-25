#!/usr/bin/env python3

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import urlparse

# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_CORPUS_DIR = "./corpora/own/docs"
DEFAULT_OUTPUT_DIR = "./audit_results"

SUPPORTED_EXTENSION = ".md"

# Stronger indicators of third-party copyrighted material.
HIGH_RISK_PATTERNS = {
    "Reprinted with permission":
        r"\breprinted (?:by|with) permission\b",

    "Reproduced with permission":
        r"\breproduced (?:by|with) permission\b",

    "Used with permission":
        r"\bused with permission\b",

    "Copyright owned by":
        r"\bcopyright (?:owned|held) by\b",

    "Third-party copyrighted material":
        r"\bthird[- ]party copyrighted (?:content|material|work|text)\b",

    "Rights reserved":
        r"\ball rights reserved\b",

    "Unauthorized reproduction":
        r"\bunauthorized reproduction\b",

    "Permission to reproduce":
        r"\bpermission (?:to|for) (?:reproduce|republish|redistribute)\b",

    "Commercial image provider":
        r"\b(?:Getty Images|Shutterstock|iStock|Adobe Stock|Alamy)\b",
}

# Indicators that may be legitimate licensing statements.
MEDIUM_RISK_PATTERNS = {
    "Copyright notice":
        r"(?:©|\bcopyright\s*(?:©)?)\s*(?:19|20)\d{2}",

    "Creative Commons license":
        r"\bcreative commons\b|\bCC[- ]BY(?:[- ](?:SA|NC|ND))*\b",

    "Content licensed from":
        r"\b(?:content|image|photograph|text|material)\s+licensed\s+from\b",

    "Image attribution":
        r"\b(?:photo|image|photograph|illustration)\s+(?:credit|courtesy)\s*:",

    "External publication attribution":
        r"\b(?:adapted|reproduced|excerpted)\s+from\b",
}

# These phrases are common in immigration, labor, and
# regulatory documents and do not establish copyright.
REGULATORY_FALSE_POSITIVES = {
    "third party works",
    "third-party worksite",
    "third party worksite",
    "third-party employer",
    "third party employer",
    "licensed by the state",
    "licensed by the department",
    "licensed by the secretary",
    "licensed by a state",
}

URL_PATTERN = re.compile(
    r"https?://[^\s<>\[\]\"']+",
    re.IGNORECASE,
)

MARKDOWN_LINK_PATTERN = re.compile(
    r"!?\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+\"[^\"]*\")?\)",
    re.IGNORECASE,
)

COMPILED_HIGH = {
    name: re.compile(pattern, re.IGNORECASE)
    for name, pattern in HIGH_RISK_PATTERNS.items()
}

COMPILED_MEDIUM = {
    name: re.compile(pattern, re.IGNORECASE)
    for name, pattern in MEDIUM_RISK_PATTERNS.items()
}


# ============================================================
# URL UTILITIES
# ============================================================

def clean_url(url):
    """
    Remove punctuation accidentally captured at the end
    of a URL in Markdown or prose.
    """
    url = url.strip()

    url = url.rstrip(".,;:!?*`'\"")

    # Remove unmatched closing parentheses.
    while url.endswith(")") and url.count(")") > url.count("("):
        url = url[:-1]

    return url


def get_hostname(url):
    try:
        return (
            urlparse(url).hostname or ""
        ).lower().rstrip(".")
    except ValueError:
        return ""


def is_us_government_url(url):
    """
    Accepts official .gov and .mil domains.

    Examples:
        irs.gov
        www.uscis.gov
        studyinthestates.dhs.gov
        aphis.usda.gov

    Does not accept:
        uscis.gov.example.com
        fake-gov.com
    """
    hostname = get_hostname(url)

    return (
        hostname.endswith(".gov")
        or hostname == "gov"
        or hostname.endswith(".mil")
        or hostname == "mil"
    )


def classify_url(url):
    hostname = get_hostname(url)

    if not hostname:
        return "invalid_url"

    if is_us_government_url(url):
        return "us_government"

    return "external"


# ============================================================
# COPYRIGHT SCANNING
# ============================================================

def get_context(text, start, end, window=140):
    context = text[
        max(0, start - window):
        min(len(text), end + window)
    ]

    return re.sub(r"\s+", " ", context).strip()


def is_regulatory_false_positive(matched_text, context):
    """
    Suppress known regulatory terminology.

    Do not suppress explicit copyright statements merely
    because they occur in a regulatory document.
    """
    matched_lower = matched_text.lower()
    context_lower = context.lower()

    if matched_lower in REGULATORY_FALSE_POSITIVES:
        return True

    # Licensing language about professional credentials
    # is not copyright licensing.
    if "licensed by" in matched_lower:
        regulatory_terms = [
            "state",
            "department",
            "secretary",
            "agency",
            "government",
            "authority",
        ]

        if any(
            term in context_lower
            for term in regulatory_terms
        ):
            return True

    return False


def scan_copyright(text, file_path):
    findings = []

    pattern_groups = [
        ("HIGH", COMPILED_HIGH),
        ("MEDIUM", COMPILED_MEDIUM),
    ]

    for severity, patterns in pattern_groups:

        for label, pattern in patterns.items():

            for match in pattern.finditer(text):

                context = get_context(
                    text,
                    match.start(),
                    match.end(),
                )

                if is_regulatory_false_positive(
                    match.group(),
                    context,
                ):
                    continue

                line_number = text.count(
                    "\n",
                    0,
                    match.start(),
                ) + 1

                findings.append({
                    "file": str(file_path),
                    "severity": severity,
                    "category": "copyright_indicator",
                    "reason": label,
                    "matched_text": match.group(),
                    "line": line_number,
                    "context": context,
                    "url": "",
                })

    return findings


# ============================================================
# EXTERNAL LINK SCANNING
# ============================================================

def scan_external_links(text, file_path):
    """
    Identify external links separately from copyrighted
    content indicators.

    A link alone does not establish that copyrighted
    material was reproduced.
    """
    findings = []
    seen_urls = set()

    for match in URL_PATTERN.finditer(text):

        url = clean_url(match.group())

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)

        if classify_url(url) != "external":
            continue

        line_number = text.count(
            "\n",
            0,
            match.start(),
        ) + 1

        context = get_context(
            text,
            match.start(),
            match.end(),
        )

        findings.append({
            "file": str(file_path),
            "severity": "INFO",
            "category": "external_reference",
            "reason": "External non-government URL",
            "matched_text": url,
            "line": line_number,
            "context": context,
            "url": url,
        })

    return findings


# ============================================================
# MARKDOWN IMAGE SCANNING
# ============================================================

def scan_markdown_images(text, file_path):
    """
    Identify embedded external images.

    An embedded image warrants more scrutiny than
    a simple hyperlink.
    """
    findings = []

    image_pattern = re.compile(
        r"!$begin:math:display$\(\[\^$end:math:display$]*)\]$begin:math:text$\(\[\^\)\\s\]\+\)\(\?\:\\s\+\\\"\[\^\\\"\]\*\\\"\)\?$end:math:text$",
        re.IGNORECASE,
    )

    for match in image_pattern.finditer(text):

        alt_text = match.group(1)
        image_url = clean_url(match.group(2))

        # Relative images need review because their source
        # and ownership cannot be determined from this file.
        is_external = (
            image_url.startswith(("http://", "https://"))
            and not is_us_government_url(image_url)
        )

        is_relative = not image_url.startswith(
            ("http://", "https://", "data:")
        )

        if not (is_external or is_relative):
            continue

        line_number = text.count(
            "\n",
            0,
            match.start(),
        ) + 1

        findings.append({
            "file": str(file_path),
            "severity": "HIGH" if is_external else "MEDIUM",
            "category": "embedded_image",
            "reason": (
                "External embedded image"
                if is_external
                else "Relative image requires provenance review"
            ),
            "matched_text": alt_text,
            "line": line_number,
            "context": get_context(
                text,
                match.start(),
                match.end(),
            ),
            "url": image_url,
        })

    return findings


# ============================================================
# DOCUMENT SCANNING
# ============================================================

def scan_document(file_path, root):
    text = file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    relative_path = file_path.relative_to(root)

    findings = []

    findings.extend(
        scan_copyright(text, relative_path)
    )

    findings.extend(
        scan_external_links(text, relative_path)
    )

    findings.extend(
        scan_markdown_images(text, relative_path)
    )

    # Remove duplicate findings.
    unique = {}

    for finding in findings:
        key = (
            finding["file"],
            finding["category"],
            finding["reason"],
            finding["line"],
            finding["matched_text"],
        )
        unique[key] = finding

    findings = list(unique.values())

    severities = {
        finding["severity"]
        for finding in findings
    }

    if "HIGH" in severities:
        priority = "HIGH"
    elif "MEDIUM" in severities:
        priority = "MEDIUM"
    elif "INFO" in severities:
        priority = "INFO"
    else:
        priority = "NO_INDICATORS"

    summary = {
        "file": str(relative_path),
        "characters": len(text),
        "findings": len(findings),
        "high_findings": sum(
            f["severity"] == "HIGH"
            for f in findings
        ),
        "medium_findings": sum(
            f["severity"] == "MEDIUM"
            for f in findings
        ),
        "external_references": sum(
            f["category"] == "external_reference"
            for f in findings
        ),
        "review_priority": priority,
        "copyright_status": "NOT_VERIFIED",
    }

    return findings, summary


# ============================================================
# CSV REPORTS
# ============================================================

FINDING_COLUMNS = [
    "file",
    "severity",
    "category",
    "reason",
    "matched_text",
    "line",
    "context",
    "url",
]

SUMMARY_COLUMNS = [
    "file",
    "characters",
    "findings",
    "high_findings",
    "medium_findings",
    "external_references",
    "review_priority",
    "copyright_status",
]


def write_csv(path, rows, columns):
    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=columns,
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Audit Markdown government documents for "
            "potential third-party copyright indicators."
        )
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_CORPUS_DIR,
        help="Directory containing downloaded Markdown files.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for audit reports.",
    )

    args = parser.parse_args()

    corpus_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    if not corpus_dir.is_dir():
        raise SystemExit(
            f"Corpus directory not found: {corpus_dir}"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    markdown_files = sorted(
        file
        for file in corpus_dir.rglob("*")
        if file.is_file()
        and file.suffix.lower() == SUPPORTED_EXTENSION
    )

    all_findings = []
    all_summaries = []
    errors = []

    print(f"\nScanning {len(markdown_files)} Markdown files...\n")

    for index, file_path in enumerate(
        markdown_files,
        start=1,
    ):
        try:
            findings, summary = scan_document(
                file_path,
                corpus_dir,
            )

            all_findings.extend(findings)
            all_summaries.append(summary)

        except Exception as exc:
            errors.append({
                "file": str(file_path),
                "error": str(exc),
            })

        if index % 50 == 0:
            print(
                f"Processed {index}/{len(markdown_files)}"
            )

    findings_path = output_dir / "copyright_audit.csv"

    summary_path = (
        output_dir / "copyright_audit_summary.csv"
    )

    write_csv(
        findings_path,
        all_findings,
        FINDING_COLUMNS,
    )

    write_csv(
        summary_path,
        all_summaries,
        SUMMARY_COLUMNS,
    )

    high = sum(
        row["review_priority"] == "HIGH"
        for row in all_summaries
    )

    medium = sum(
        row["review_priority"] == "MEDIUM"
        for row in all_summaries
    )

    info = sum(
        row["review_priority"] == "INFO"
        for row in all_summaries
    )

    clean = sum(
        row["review_priority"] == "NO_INDICATORS"
        for row in all_summaries
    )

    print("\n========== COPYRIGHT AUDIT ==========")
    print(f"Documents discovered: {len(markdown_files)}")
    print(f"Documents scanned:    {len(all_summaries)}")
    print(f"High priority:        {high}")
    print(f"Medium priority:      {medium}")
    print(f"External links only:  {info}")
    print(f"No indicators:        {clean}")
    print(f"Scan errors:          {len(errors)}")
    print(f"Total findings:       {len(all_findings)}")
    print("=====================================")

    print(f"\nFindings: {findings_path}")
    print(f"Summary:  {summary_path}")

    if errors:
        print("\nFiles that could not be scanned:")
        for error in errors:
            print(f"  {error['file']}: {error['error']}")

    print(
        "\nNote: NO_INDICATORS does not mean copyright-free. "
        "The audit identifies material requiring review."
    )


if __name__ == "__main__":
    main()