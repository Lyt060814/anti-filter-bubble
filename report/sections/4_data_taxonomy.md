# 4 Data and the Distribution of Opposing Narratives (RQ1)

<!-- D4 draft, Zhao Dingcheng, 2026-11-07. 4.1 and 4.4 are Li Yitong's parts (data, engagement); 4.2 and 4.3 are Zhao Dingcheng's (taxonomy, label quality).
Numbers in 4.2 come from Qwen labels of the bottom-up sample and are provisional: Li Yitong will relabel the same 3,000 impressions with DeepSeek V4 Pro and a v1-style prompt, and Table 4.1 will be regenerated with
  python -I -X utf8 analysis/v6_annotation/taxonomy.py <new labels csv> <source name>
Numbers in 4.3 are for prompt v0 and will be replaced by the v1 check. -->

## 4.1 Data

*(Li Yitong: RecIF logs, video descriptions, issue candidates, sampling.)*

## 4.2 Which issues carry opposing narratives

**How the taxonomy was built.** Rather than starting from a list of issues we expected to matter, we let the data show which social issues users actually see. We drew 3,000 impressions uniformly from RecIF user histories, so each video appears in proportion to how often it was shown, and asked an open LLM (Qwen3-30B-A3B-Instruct-2507) to label each one from its text description: the broad domain, a short name for the specific issue, whether the video expresses or reinforces a contested position, and if so which of four narrative types it uses. 2,996 outputs were valid. The four types are:

- **Only-right-way**: one choice is presented as the only proper path, and other choices are belittled.
- **Binary opposition**: a question is framed as having exactly two opposed camps or options.
- **Anxiety-raising**: fear, urgency or shame is used to push a view or a choice.
- **Group label**: a whole social group (by gender, region, age and so on) is portrayed negatively, or a single case is presented as typical of the group.

The full definitions, with decision steps and borderline cases, are in Appendix A. The model writes the issue name as free text, and most names occur only once, so we grouped them into sub-issues with fixed keyword rules applied to the model's own labels; about a fifth of the issue names in the five domains we study match no rule and are left as "other".

**Table 4.1.** Social-issue domains in an exposure-weighted sample of 2,996 RecIF impressions (labels: Qwen3-30B, not yet checked against a stronger model). Opposing share is the proportion of the domain's impressions labelled as expressing a contested position, with a 95% Wilson interval. Domains marked * are studied in this report.

| Domain | Share of exposures | Opposing narrative (within domain) | Main narrative types (count) | Largest sub-issues (n) |
|---|---:|---:|---|---|
| Non-issue content | 77.7% | — | — | — |
| Culture and values | 5.5% | 44% (72/164; 37%–52%) | only-right-way (26), group label (17), binary opposition (15), anxiety-raising (14) | history and national memory (23); images of women and men (20); tradition and heritage (13) |
| Family and generations * | 3.6% | 31% (34/108; 23%–41%) | binary opposition (13), only-right-way (11), anxiety-raising (7), group label (3) | parenting and parent-child relations (50); family conflict and violence (16); in-laws and marrying into a family (9) |
| Gender and relationships * | 3.3% | 63% (62/98; 53%–72%) | binary opposition (22), anxiety-raising (20), only-right-way (11), group label (9) | dating, break-ups and feelings (61); marriage and spouses (15); gender roles and expectations (10) |
| Consumption and money * | 3.1% | 41% (38/93; 31%–51%) | anxiety-raising (27), only-right-way (8), binary opposition (3) | promotions and marketing (29); spending values and personal finance (19); prices and housing (11) |
| Study and ideas | 1.5% | 24% (11/45; 14%–39%) | anxiety-raising (4), binary opposition (3), only-right-way (2), group label (2) | exam and study pressure (26) |
| Body and appearance * | 1.4% | 88% (36/41; 74%–95%) | anxiety-raising (27), only-right-way (4), binary opposition (4), group label (1) | appearance anxiety (37) |
| Life choices and paths * | 1.3% | 39% (15/38; 26%–55%) | only-right-way (8), anxiety-raising (6), binary opposition (1) | striving, lying flat and life direction (12); jobs and careers (9); exams and study paths (6) |
| Other social issues | 1.3% | 55% (21/38; 40%–70%) | anxiety-raising (11), only-right-way (4), group label (4), binary opposition (2) | crime and public safety (11); history and war (9); health (8) |
| Public order and freedom | 0.9% | 62% (16/26; 43%–78%) | anxiety-raising (8), only-right-way (3), group label (3), binary opposition (2) | safety and surveillance (11); policing and law enforcement (7) |
| Resources and fairness | 0.6% | 53% (9/17; 31%–74%) | only-right-way (4), binary opposition (2), anxiety-raising (2), group label (1) | — |

**Reading the table.** About one impression in five (22.3%) touches a social issue, and the five domains we study together account for 12.6% of all impressions. Within them the narrative mix differs. Body and appearance is almost entirely anxiety-raising, mostly about looks. Of the four domains with more than 90 impressions, gender and relationships has the highest share of opposing narratives and the widest spread of types, and it has more group labels than any domain except culture and values; this, together with its size, is why we use it for the case study in Section 5. In consumption, many "anxiety-raising" labels fall on promotions: at least 10 of the 27 are in the promotions sub-issue, which is why our annotation rules (Appendix A) exclude marketing from every narrative type.

These shares should be read with two cautions. First, each domain has only 17 to 164 impressions, so the intervals are 15 to 43 percentage points wide. Second, they come from an open model that, in our check on marriage videos (Section 4.3), labelled far more videos as carrying a narrative than a stronger reference model did. The table therefore shows *where* opposing narratives concentrate and *what kind* they are; their levels will be re-estimated with the stronger model.

**Typical disputes.** The following are illustrative paraphrases of the kind of argument found in each studied domain, written by us from the issue labels; they are not quotations from videos.

- *Gender and relationships*: whether how much a partner spends on dates shows how much they care; whether a woman should keep her own income after marriage. A group-label version: "men from poor rural families bring their whole family into the marriage".
- *Body and appearance*: whether clear skin, a slim body or greater height is needed to be treated well; videos often push a quick fix with a warning about what happens otherwise.
- *Family and generations*: strict versus relaxed parenting; how much grown children owe their parents; conflict between a wife and her mother-in-law.
- *Life choices and paths*: taking the postgraduate or civil-service exam versus starting work; "lying flat" versus striving.
- *Consumption and money*: saving versus enjoying life now; whether a home must be bought before marriage.

**What we left out, and why.** We exclude three groups of content from the main analysis. (1) *History, national memory and patriotism* (the largest sub-issue in culture and values, and part of other social issues) and *policing, surveillance and campus control* (public order and freedom). These are politically sensitive: we expect labels to disagree more, and both the ethics of studying users' exposure to them and open discussion of results are harder. (2) *Resources and fairness* and *study and ideas*, which are small (17 and 45 impressions) or carry few opposing narratives (24%), and overlap with life choices. (3) The remaining culture-and-values content, which is a broad mix of self-identity, tradition and fan culture with no common dispute. Its "images of women and men" sub-issue (20 impressions) overlaps with gender and relationships, and we report it there when the stronger-model labels are available.

## 4.3 How reliable the labels are

No video was labelled by hand. To estimate label quality we had the open model and a stronger reference model (DeepSeek V4 Pro) label the same 500 marriage-and-family videos independently, sampled in proportion to exposures; a third model (GPT-6.1 Sol) labelled the first 150 as a second reference. With the first version of the prompt, the open model flagged 4.0% of videos as carrying a gender group label and the reference flagged 1.4% (95% interval 0.7%–2.9%). Only two videos were flagged by both. Taking the reference as the standard, the open model's precision was 10% (2/20; 95% interval 3%–30%) and its recall 29% (2/7; 8%–64%). Raw agreement was 95%, but only because group labels are rare; Cohen's kappa was 0.13. Two outputs from the open model were invalid and are reported as missing.

Reading the two models' one-line reasons, most of the open model's false positives fell into three patterns: a family role, such as a mother-in-law or a stepmother, treated as a whole gender (7 of 18); a single character's behaviour in a drama treated as a claim about the group (5); and teasing treated as disparagement (3). We revised the prompt twice in response (Appendix A.4). The first revision moved the two models in opposite directions: the open model flagged half of all videos and the reference model fewer than before. The second revision makes the model answer four yes-or-no questions, each aimed at one of these errors, as separate fields before it gives a label, and rejects outputs whose label does not follow from the answers.

This check has a clear limit: the reference is itself a model, not a human gold standard. Errors shared by both models, for example cues that appear only in the video and not in its description, cannot be detected. The reference flagged only 7 videos, so recall is estimated imprecisely.

*(To be updated with the revised-prompt results and an enlarged set of reference positives.)*

## 4.4 Do opposing narratives attract more engagement?

*(Li Yitong: completion, like and "not interested" rates by narrative type.)*
