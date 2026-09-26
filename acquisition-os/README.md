# Acquisition OS — Companies House Universe

This job discovers the latest official Companies House monthly basic-company snapshot, downloads the split ZIP files sequentially, and streams the CSV rows.

It keeps only companies that are:
- status **Active**;
- at least **5 years old** at the snapshot date;
- matched to Acquisition Buy Box V1 SIC rules.

No Companies House data is committed to Git. The filtered CSV and summary are returned only as a short-lived GitHub Actions artifact.

The workflow does **not** contact owners, send messages, make offers, or perform financial actions.
