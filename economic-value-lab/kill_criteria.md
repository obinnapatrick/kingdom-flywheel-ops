# Kill Criteria

Kill criteria run **before** the rubric. A candidate that trips a hard kill is removed from
scoring regardless of how attractive it looks. A candidate that trips a soft kill is suspended
until the named evidence is found. Every kill is logged in `candidate_ledger.csv` and
`decision_record.md` with the criterion ID and the evidence used.

Thresholds are calibrated to the operating assumptions in `CLAUDE.md` (solo operator, limited
capital, no licences, UK-based). If those change, re-run the kills.

## Hard kills

| ID | Criterion | Test (trips if…) | Why it is a kill, not a low score |
|---|---|---|---|
| K1 | **Impossible access** | No plausible path for a solo operator to reach the workflow and its data within 60 days without privileged relationships. | Without access there is no experiment, so no learning. |
| K2 | **Unmeasurable outcome** | The value cannot be expressed as cash, time or output with a baseline we could obtain. | The lab's objective is *verified* value. |
| K3 | **Tiny capturable value** | Realistically capturable value per buyer is below ~£5k/yr *and* there is no credible way to aggregate many buyers cheaply. | Cost of acquiring and serving a buyer exceeds the value. |
| K4 | **No economic buyer** | Nobody with budget authority both feels the loss and can pay to fix it. | Pain without a payer produces gratitude, not revenue or evidence of value. |
| K5 | **Proof cycle too long** | First credible evidence of value (not just activity) cannot arrive within ~6 months. | We need many learning cycles; long cycles starve the lab. |
| K6 | **Solved cheaply already** | An incumbent solution addresses the problem at low cost for most of the affected population, and no underserved segment has been identified. | Residual value is too small and contested. |
| K7 | **Licence precondition** | Proof requires a regulated status we do not hold (e.g. SRA reserved legal activity, FCA-authorised claims management in a regulated sector, clinical safety sign-off, handling US PHI as a covered entity/business associate). | Legal exposure and cost before any evidence. |
| K8 | **Capital precondition** | More than ~£25k of capital (hardware, licences, staff) is needed before the first evidence of value. | Beyond the operator's assumed means. |
| K9 | **Causation not attributable** | Outcome is dominated by confounders and no counterfactual (control group, look-back recovery, A/B, pre/post with stable baseline) can be designed. | We could not tell whether we created value. |
| K10 | **Misaligned incentives** | The party that bears the loss cannot act on it, and the party that can act does not bear it, with no mechanism to bridge them. | Interventions will not be adopted. |
| K11 | **Vanishing problem** | Legislation, regulation or platform change already committed is likely to remove most of the problem within ~24 months. | We would build knowledge for a disappearing arena. |
| K12 | **Hype dependency** | Core value depends on capabilities that do not demonstrably exist today. | Violates evidence-over-enthusiasm. |
| K13 | **Safety-critical failure mode at proof stage** | An error in our intervention could plausibly harm people physically or medically during the experiment. | Asymmetric downside. |
| K14 | **Extractive or reputationally toxic** | Value comes mainly from exploiting a counterparty's weakness, claims-farming or behaviour that would damage trust if public. | Destroys the trust the lab needs to compound. |
| K15 | **Enterprise-only sales** | Every buyer is a large organisation or public body whose procurement cycle is routinely > 9 months. | Incompatible with K5 and a solo operator. |
| K16 | **Structural bottleneck** | After cheap incumbent tools, the residual problem is caused by power, law or market structure that no operator intervention can change. | Nothing we could build moves the outcome. |
| K17 | **No transferable learning** | Success or failure would teach nothing reusable outside this narrow case. | Violates objective 10 (learning value even if it fails). |
| K18 | **Single-gatekeeper dependency** | One platform or counterparty can unilaterally remove the opportunity (e.g. one marketplace's reimbursement policy). | The arena can disappear overnight. |

## Soft kills (suspend, do not score)

| ID | Criterion | Exit condition |
|---|---|---|
| S1 | **Vendor-only evidence** — every magnitude comes from parties selling a solution. | One independent source (official, academic, trade body, regulator) corroborates order of magnitude. |
| S2 | **Unverifiable magnitude** — the size cannot be bounded even roughly. | A derivation from primary inputs gives a range within ~10×. |
| S3 | **Unknown buyer** — pain is evidenced but who pays is unclear. | A named role with budget authority is identified from evidence (job ads, procurement records, pricing of existing services). |

## Anti-gaming rules

- A candidate cannot be rescued from a hard kill by narrowing it *after* the kill without
  re-entering it as a **new** candidate row with its own evidence.
- Kills are applied by the evidence, not by the score. A high-scoring idea that trips K7 is dead.
- Partial kills are recorded: when a sub-problem trips a kill (e.g. retentions under K11), note
  it on the parent candidate and remove that sub-problem from the value estimate.
