# Internal Scoring Logic: STAR Impact Score (Admin Only)

This document outlines the internal, bias-based scoring calculation used to determine the STAR Impact Score for universities. This data is intended for administrative review and filters out spam/suspicious entries to ensure merit-based rankings.

## Rubric and Weighting

| Component | Weight | Description |
| :--- | :--- | :--- |
| **Total Members** | 20% | Raw count of registered individuals from the institution. |
| **Quality Gate** | 10% | Only members marked as **"AUTHENTIC"** are counted (Agent Review). Filters out spam/suspicious entries. |
| **Engagement** | 20% | Based on Profile Completion Rate. (Avg. Completion % / 10). Higher profile completion indicates active commitment. |
| **AI Readiness** | 10% | Measured via AI Enthusiasm score (participation in AI-related circles and workshops). |
| **STAR Awards Won** | 30% | Recognition of high-impact contributions. (Note: OP Jindal University, American University in the Emirates, and Algoma University are current winners). |
| **Professional Diversity** | 5% | Number of distinct academic fields/professions represented by the institution's members. |
| **Year Joined** | 5% | Average enrollment vintage. Earlier records (e.g., 2023) receive higher scores than recent ones (e.g., 2025). |

## Calculation Formula

The STAR Impact Score (out of 100) is calculated as:
`(TotalMembers_Score * 0.20) + (AuthenticRange_Score * 0.10) + (ProfileCompletion_Score * 0.20) + (AIReadiness_Score * 0.10) + (Awards_Score * 0.30) + (Diversity_Score * 0.05) + (Vintage_Score * 0.05)`

> [!IMPORTANT]
> This internal breakdown is not visible to the general public. The public-facing "STAR Impact Score" is the normalized result of this comprehensive evaluation.
