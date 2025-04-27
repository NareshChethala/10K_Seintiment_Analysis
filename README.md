# Sentiment Analysis on SEC 10-K Filings
**Comparing Lexicon-Based and Transformer-Based Sentiment Analysis Techniques**

---

## 📁 Project Overview

This project investigates the application of sentiment analysis methods to large-scale financial documents — specifically, SEC 10-K annual filings.

We systematically compare:
- **Loughran-McDonald (LM) Lexicon-Based Approach** 
- **Transformer-Based FinBERT Model**

across full document text and major sections (Item 1: Risk Factors, Item 7: Management Discussion, Item 7A: Quantitative Disclosures).

Our goal is to evaluate how these two techniques perform on lengthy, domain-specific financial narratives, focusing on both **numerical scores** and **classification agreement**.

---
## ⚙️ Methods Used

- **Data Extraction**:  
  - SEC EDGAR crawler and BeautifulSoup parsing
- **Preprocessing**:  
  - HTML cleaning, whitespace removal, section parsing
- **Sentiment Analysis**:  
  - **LM Dictionary** for word-count-based sentiment scoring
  - **FinBERT Transformer** for deep contextualized sentiment scoring
- **Summarization (Optional Extension)**:  
  - BART-large-CNN model used to create summarized versions for experimental analysis
- **Statistical Analysis**:
  - Pearson Correlation
  - Paired Samples t-Test
  - Agreement Rate Calculation
- **Visualization**:
  - Scatter Plots, Class Distribution Comparison, Agreement Rate Bar Charts
- **Tools**:  
  - Python, NLTK, Transformers (HuggingFace), Matplotlib, Seaborn, Pandas, LaTeX

---

## 📊 Key Findings

- **Moderate positive correlation** between LM and FinBERT sentiment scores.
- **FinBERT generally assigns higher (less negative) sentiment** than LM.
- **Significant differences** in sentiment detection especially for risk-related sections (Item 1 and Item 7A).
- **Agreement rates** between methods range between **61\%–68\%** across sections.
- **LM tends toward neutral labeling**, whereas FinBERT identifies more positive tone in financial narratives.

---

## 🏆 Highlights

- Full-document and section-level comparative analysis
- Real 10-K filings from S&P 500 companies
- Statistical robustness (t-tests and correlation)
- Reproducible codebase and clear documentation
- Visualization-ready figures (300dpi quality for publishing)

---

## 📚 References

- Loughran, T., & McDonald, B. (2011). *When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks.* Journal of Finance.
- Araci, D. (2019). *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models.* arXiv.
- Huang, A., Lin, C., Wang, Z., & Zuo, L. (2020). *Machine Learning and Financial Statement Analysis: Quantifying Risk-Return Trade-Offs Using 10-K Filings.*
- Pang, B., & Lee, L. (2008). *Opinion Mining and Sentiment Analysis.*
- Hu, M., & Liu, B. (2004). *Mining Opinion Features in Customer Reviews.*

---

## 🚀 How to Reproduce

1. Clone/download the repository
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the notebooks inside `code/` sequentially:
   - Start with `10k_scraping_and_cleaning.ipynb`
   - Then move to `lm_sentiment_analysis.ipynb`
   - Apply `finbert_sentiment_analysis.ipynb`
   - Conduct statistical visualization with `statistical_analysis_visualization.ipynb`
4. Compile the LaTeX file to generate the final paper.

---

## 📬 Contact

- **Author**: Naresh Chethala
- **Collaborators**: Furqan Ahmed, Sai Harshith
- **Email**: [Your Email Here] (Optional)

---
