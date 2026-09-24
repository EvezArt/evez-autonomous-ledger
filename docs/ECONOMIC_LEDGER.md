# EVEZ Economic Ledger

This layer tracks assets, resources, IP, money received, receivables, crypto,
expenses, liabilities, and opportunities without conflating potential value with
realized value.

Core invariant:

    CLAIMED VALUE != REALIZED VALUE

A value contributes to the verified economic position only when it has supporting
evidence references and a verified/supported valuation status.

Categories:

- FIAT: actual currency balance or received funds.
- REVENUE: money actually received.
- RECEIVABLE: contractually owed money not yet received.
- CRYPTO: actual crypto holdings when verified by evidence.
- ASSET/RESOURCE/IP: controlled value with provenance.
- LIABILITY/EXPENSE: obligations or money actually spent.
- OPPORTUNITY: potential future value, never included in realized position.
- UNKNOWN: insufficient evidence or classification.

The summary computes:

    realized cash
  + verified receivables
  + verified liquid assets
  + verified controlled resources
  - verified liabilities
  = realized economic position

This is an accounting/provenance model, not a claim that an entry has any market
value beyond its supplied evidence and valuation method.
