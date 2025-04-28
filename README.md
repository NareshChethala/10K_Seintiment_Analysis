# Sentiment Analysis on SEC 10-K Filings
**Comparing Dictionary-Based and Transformer-Based Methods**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview
This study analyzes sentiment in SEC 10-K filings by comparing two approaches:
- **Lexicon-based method**: Loughran-McDonald (LM) Financial Sentiment Dictionary.
- **Transformer-based model**: FinBERT, a fine-tuned version of BERT for financial texts.

We systematically evaluated sentiment at:
- **Section level**: Item 1 (Business), Item 7 (Management Discussion), Item 7A (Quantitative Disclosures).
- **Full-document level**: Entire 10-K filings.

The project explores how well each method captures financial sentiment and discusses their strengths, weaknesses, and real-world implications.

---

## Methodology

- **Data Collection**: 10-K filings scraped from SEC EDGAR database.
- **Preprocessing**: Cleaning HTML, extracting text, tokenization, and segmentation.
- **Sentiment Analysis**:
  - **LM Method**: Computed positive, negative, and net sentiment percentages.
  - **FinBERT Model**: Classified text chunks as Positive, Neutral, or Negative, aggregated into overall scores.
- **Statistical Comparison**:
  - Pearson correlation analysis
  - Paired samples t-tests
  - Confusion matrix analysis
  - Class distribution comparison
  - Agreement rate calculation

---

## Key Results

- **Correlation**: Moderate positive correlations between LM and FinBERT (r ≈ 0.45).
- **Sentiment Scores**: FinBERT detects slightly more optimistic tones compared to LM.
- **Agreement Rates**: Ranged from 21.4% to 89.2% depending on section.
- **Confusion Matrix**: Highlighted that FinBERT is more sensitive to subtle negative cues missed by LM.

---

## Visualizations
- Correlation scatter plots between LM and FinBERT.
- Sentiment class distribution bar charts.
- Agreement rate bar chart.
- Full-document level confusion matrix.

All visualizations were generated using Matplotlib and Seaborn.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/NareshChethala/10K_Seintiment_Analysis.git
   cd 10K_Sentiment_Analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open and run the notebook:
   ```
   code/sentiment_analysis_10k.ipynb
   ```
4. Compile the LaTeX document to generate the final paper.

---

## Keywords
`Sentiment Analysis`, `Financial NLP`, `SEC 10-K Filings`, `Loughran-McDonald Lexicon`, `FinBERT`, `Transformer Models`, `Lexicon-Based Methods`, `Financial Text Mining`

---

## References
Key references include:
- Loughran & McDonald (2011) \u2014 Financial Sentiment Lexicon
- Devlin et al. (2019) \u2014 BERT: Pre-training Deep Bidirectional Transformers
- Araci (2019) \u2014 FinBERT for Financial Sentiment Analysis
- Huang et al. (2020) \u2014 Machine Learning and Financial Text Analysis
- Pang & Lee (2008) \u2014 Opinion Mining and Sentiment Analysis

(Full references are available in the paper.)

---

## License

This project is licensed under the [MIT License](LICENSE).

© 2025 Naresh Chethala. All rights reserved.

## Contact

If you have any questions, feedback, or collaboration opportunities, feel free to reach out:

- 📧 Email: [nareshchethala99@outlook.com](mailto:nareshchethala99@outlook.com)
- 🌐 GitHub: [@NareshChethala](https://github.com/NareshChethala)

---
