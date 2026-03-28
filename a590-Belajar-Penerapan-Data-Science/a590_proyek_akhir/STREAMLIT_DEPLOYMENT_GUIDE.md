# 🚀 Deployment Guide - Streamlit Cloud

## Quick Start - Deploy ke Streamlit Cloud

### Prasyarat:
- GitHub account
- Streamlit Cloud account (kosong, gratis)
- Repository di GitHub dengan struktur benar

### Langkah-langkah Deployment:

#### 1. **Pastikan Repository Structure Benar**
```
a590-Belajar-Penerapan-Data-Science/
└── a590_proyek_akhir/
    ├── app.py                           (Main Streamlit application)
    ├── requirements.txt                 (Python dependencies)
    ├── student_data_metabase_final.csv  (Dataset - CRITICAL)
    ├── dataset_with_predictions.csv     (Backup dataset)
    ├── model/                           (Model artifacts)
    │   ├── student_status_model.joblib
    │   ├── scaler.joblib
    │   ├── label_encoders.joblib
    │   ├── le_target.joblib
    │   └── feature_names.joblib
    ├── .streamlit/
    │   ├── config.toml
    │   └── streamlit.app
    └── README.md
```

#### 2. **Update GitHub Repository**
```bash
git add .
git commit -m "Feat: Fix dataset loading paths for Streamlit Cloud deployment"
git push origin main
```

#### 3. **Deploy ke Streamlit Cloud**

**Option A: GUI (Recommended)**
1. Go to https://share.streamlit.io
2. Click "New app" button
3. Fill in the details:
   - **Repository**: `2200018178-FIRIZKI/Proyek-Akhir-Penerapan-Data-Science-Indosat`
   - **Branch**: `main`
   - **Main file path**: `a590_proyek_akhir/app.py`
4. Click "Deploy"

**Option B: Command Line (If available)**
```bash
streamlit run app.py --deploy
```

#### 4. **Verify Deployment**
- Monitor the deploy logs in Streamlit Cloud dashboard
- Check for any errors related to:
  - Missing dependencies in `requirements.txt`
  - Missing data files
  - Model file issues

#### 5. **Troubleshooting**

**Issue: Dataset not found**
- Solution: Ensure `student_data_metabase_final.csv` is in `a590_proyek_akhir/` folder
- Fallback: App will use `dataset_with_predictions.csv` if primary dataset not found

**Issue: Model loading error**
- Solution: Verify all `.joblib` files are in `model/` subdirectory
- Check: `feature_names.joblib`, `label_encoders.joblib`, `le_target.joblib`, `scaler.joblib`, `student_status_model.joblib`

**Issue: Requirements/Dependencies missing**
- Solution: Update `requirements.txt` with all dependencies
- Command: `pip freeze > requirements.txt`

---

## ✅ Deployment Checklist

- [ ] GitHub repository updated with latest changes
- [ ] All data files present in correct directories
- [ ] All model artifacts in `model/` folder
- [ ] `requirements.txt` includes all dependencies
- [ ] `.streamlit/config.toml` configured correctly
- [ ] `app.py` loads data from multiple possible paths
- [ ] Tested locally before pushing: `streamlit run app.py`
- [ ] Deployment successful in Streamlit Cloud

---

## 📝 Dataset Location Best Practices

**For Streamlit Cloud:**
1. Always place CSV files in the same directory as `app.py`
2. Use relative paths: `./filename.csv`
3. Provide multiple fallback paths in code

**For Local Development:**
1. Use `os.path.dirname(__file__)` for paths relative to script
2. Support multiple path variations
3. Show warnings if primary dataset not found

---

## 🔗 Links

- **Deployed App**: https://share.streamlit.io/[your-app-link]
- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Repo**: https://github.com/2200018178-FIRIZKI/Proyek-Akhir-Penerapan-Data-Science-Indosat

---

**Last Updated**: March 28, 2026
**Status**: ✅ Ready for Deployment
