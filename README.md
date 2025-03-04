# 📌 RPL-IDS-Behavior-Dataset
### Intrusion Detection System for RPL-based IoT Networks

This repository provides **a dataset and IDS framework** for detecting attacks in **RPL-based IoT networks**.  
It includes:
- **Contiki-NG modifications** to simulate attack scenarios.
- **Python scripts** for dataset generation, machine learning evaluation, and feature analysis.

---

## 📂 Repository Structure
```
RPL-IDS-Behavior-Dataset/
│── contiki-ng/              # Modified Contiki-NG files (must replace existing Contiki-NG installation)
│── python-analysis/         # Python scripts for dataset processing & IDS evaluation
│   ├── dataset/             # Processed dataset (CSV files)
│   ├── dataset-processing/  # Python scripts to generate dataset from logs
│   ├── ids-evaluation/      # IDS testing and ML classification scripts
│   ├── feature-selection/   # Feature importance analysis scripts
│── README.md                # Project documentation
│── LICENSE                  # License file (optional)
│── .gitignore               # Ignore unnecessary files
```

---

## ⚙️ Installation & Setup

### **1️⃣ Install Contiki-NG**
Ensure you have **Contiki-NG** installed on your machine. If not, follow the official guide:  
🔗 [Contiki-NG Installation Guide](https://github.com/contiki-ng/contiki-ng)

### **2️⃣ Replace Contiki-NG Files**
To apply the necessary modifications for attack simulation:
1. **Copy the entire `contiki-ng/` folder** from this repository.
2. **Paste it into your existing Contiki-NG installation**, replacing all files:
   ```
   cp -r contiki-ng/* ~/contiki-ng/
   ```
   _(Replace `~/contiki-ng/` with your actual Contiki-NG installation path.)_

### **3️⃣ Open Cooja Simulator**
After replacing the files, launch Cooja:
```
cd ~/contiki-ng/tools/cooja
ant run
```

---

## 🚀 Running the Simulation
1. Inside Cooja, open the provided `.csc` simulation files from `contiki-ng/cooja-simulations/`.
2. Click **Start** to run the network simulation.
3. The modified nodes will generate log files containing network behavior.

---

## 📊 Dataset Generation & IDS Testing

Once simulation logs are collected, use Python scripts for dataset processing and IDS evaluation.

### **1️⃣ Process Simulation Logs**
Convert logs into a structured dataset:
```
cd python-analysis/dataset-processing
python dataset_generation.py
```

### **2️⃣ Run IDS Evaluation**
Test the **Intrusion Detection System (IDS)** using machine learning models:
```
cd ../ids-evaluation
python ids_evaluation.py
```

### **3️⃣ Analyze Feature Importance**
To understand which features contribute most to attack detection:
```
cd ../feature-selection
python feature_importance.py
```

---

## 📄 Dataset Description
The dataset contains:
- **Node-specific features** (e.g., RPL rank, version number, packet counts).
- **Neighbor-aggregated features** (e.g., average forwarded packets).
- **Derived features** (e.g., rank difference, control-to-data packet ratio).

For full details, refer to the dataset documentation in `python-analysis/dataset/README.md`.

---

## 📜 License
This project is released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 📬 Contact & Contributions
- **Author:** HUNSR  
- **GitHub Issues:** [Submit a Bug Report](https://github.com/HUNSR/RPL-IDS-Behavior-Dataset/issues)  
- **Pull Requests:** Contributions are welcome! Feel free to open a PR.

---

