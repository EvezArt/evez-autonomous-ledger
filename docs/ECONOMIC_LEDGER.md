# EVEZ Economic Ledger

This layer tracks assets, resources, IP, revenue, receivables, crypto, fiat,
expenses, liabilities, and opportunities without conflating financial flows with
a balance-sheet-style position.

Core invariant:

    CLAIMED VALUE != REALIZED VALUE

A value enters the verified economic position only when it has evidence references
and a VERIFIED/SUPPORTED valuation status.

The accounting model deliberately separates:

- `FIAT`: verified currency balance.
- `CRYPTO`: verified liquid crypto value.
- `REVENUE`: money actually received, tracked as a flow.
- `EXPENSE`: money actually spent, tracked as a flow.
- `RECEIVABLE`: money owed but not yet received.
- `ASSET/RESOURCE/IP`: controlled value with evidence.
- `LIABILITY`: outstanding obligation.
- `OPPORTUNITY`: possible future value, never included in realized position.

Summary:

    realized revenue - realized expenses
        = net cash flow

    fiat
  + crypto
  + receivables
  + verified controlled resources
  - liabilities
        = realized economic position

Revenue is not added to the cash balance because doing so would count the same
money twice when the cash balance already contains the proceeds. Humanity has
invented double-entry accounting and then spent centuries trying to defeat it
with spreadsheets, so the code will at least behave itself.

No market valuation is inferred by this module. Every valuation needs its supplied
method and evidence.
