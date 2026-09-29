# Evidence store

Unsupported claims are not evidence. This folder separates what we know from what we were told.

## Structure

```
evidence/
  README.md               — this file: rules and structure
  source_register.csv     — every source used, one row per source (S01…), with independence and caveats
  candidates/
    C25_import_duty_recovery.md
    C27_subcontractor_cash_cycle.md
    C02_retailer_deductions.md
    C26_out_of_hours_energy.md
    killed_and_weak_survivors.md — short evidence notes for the rest
```

## Rules

1. **One source, one row** in `source_register.csv`. Record: publisher type, whether it is
   independent of anyone selling a solution, how it was retrieved, and caveats.
2. **Retrieval honesty.** `retrieval = search excerpt` means we saw a search engine's summary of the
   source, not the document. Such claims are `REPORTED`, never `FACT`. In Phase Zero the network
   policy blocked direct retrieval of most primary documents, so **no claim in this folder is
   currently labelled `FACT`.**
3. **Every candidate file has four sections:** Supporting evidence · Disconfirming evidence ·
   Estimates (with arithmetic) · Open gaps. A file without disconfirming evidence is incomplete.
4. **Vendor evidence** (anyone selling a fix) may indicate that a problem is being sold against. It
   cannot establish magnitude on its own (kill criterion S1).
5. **Never overwrite.** When evidence changes, append a dated entry; keep the old claim struck
   through with the reason.
6. **Link every number** in other files back to a source ID or an estimate in a candidate file.
