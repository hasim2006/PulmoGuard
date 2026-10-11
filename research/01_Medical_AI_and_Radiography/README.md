# 🩻 Domain 01: Medical AI & Clinical Radiography

This domain comprises peer-reviewed scientific literature detailing the implementation of artificial intelligence, convolutional neural networks (CNNs), and transfer learning for biomedical image classification.

---

## 📄 Key Papers & Publications

### 1. Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning
- **Authors:** Daniel S. Kermany, Michael Goldbaum, Wenjia Cai, et al.
- **Journal:** *Cell* (Volume 172, Issue 5, Pages 1122–1131.e9, February 2018)
- **DOI:** [10.1016/j.cell.2018.02.010](https://doi.org/10.1016/j.cell.2018.02.010)
- **PubMed:** [PMID: 29474911](https://pubmed.ncbi.nlm.nih.gov/29474911/)
- **Local File:** [`Identifying-Medical-Diagnoses-and-Treatable-Diseas.pdf`](Identifying-Medical-Diagnoses-and-Treatable-Diseas.pdf)
- **Abstract Summary:**
  Demonstrates an AI framework utilizing deep convolutional neural networks with transfer learning to diagnose ophthalmic conditions (diabetic retinopathy and choroidal neovascularization) and pediatric bacterial vs. viral pneumonia on chest radiographs. The model achieved performance comparable to board-certified radiologists, establishing the definitive Kaggle Chest X-Ray dataset leveraged in this project.
- **Relevance to PulmoGuard:**
  Forms the foundational dataset (5,856 pediatric chest X-rays) and clinical baseline for PulmoGuard's classification pipeline.

---

### 2. Learning from Everyday Images Enables Expert-like Medical Diagnosis
- **Authors:** Andre Esteva, Brett Kuprel, Roberto A. Novoa, et al.
- **Journal:** *Cell Press / Nature Reviews Insights*
- **DOI:** [10.1038/nature21056](https://doi.org/10.1038/nature21056)
- **Local File:** [`Learning-from-Everyday-Images-Enables-Expert-like-.pdf`](Learning-from-Everyday-Images-Enables-Expert-like-.pdf)
- **Abstract Summary:**
  Explores how pre-training deep neural architectures (e.g., ImageNet, VGG16, Inception) on millions of everyday non-medical objects equips models with generalized edge, texture, and contour detectors. Fine-tuning these weights on specialized biomedical imaging achieves expert-level dermatological and radiographic diagnostic sensitivity.
- **Relevance to PulmoGuard:**
  Validates PulmoGuard's VGG16 transfer learning architecture and low-level feature extraction for pulmonary consolidation detection.
