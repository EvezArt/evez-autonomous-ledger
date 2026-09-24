# Reality Gate Integration Contract

The Autonomous Ledger is the accounting/audit projection. It should consume Reality
Kernel receipts rather than infer authorization from an agent's narrative.

Record at minimum:

- envelope hash
- actor
- target
- requested effect
- authority
- evidence references
- policy version
- decision
- drift score
- execution status
- Event Spine sequence

Important invariant:

    DECLARED != EFFECTIVE

A ledger entry that claims an authorization was granted is not proof that the runtime
actually granted it. Preserve both the requested/declarative record and the observed
effective outcome.

Source implementation:
https://github.com/EvezArt/evez-event-spine
