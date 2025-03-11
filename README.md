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
│   ├── IDS-example/         # Example IDS-related code and network topology simulator files
│   ├── os/                  # Core OS files and RPL protocol modifications (replace existing Contiki-NG files)
│── python-analysis/         # Python scripts for dataset processing & IDS evaluation
│   ├── dataset/             # Log files generated from simulation (raw data)
│   ├── feature-selection/   # Feature importance analysis scripts
│── dataset_generation.py    # Script to read log files from dataset/ folder and generate the final dataset
│── README.md                # Project documentation and usage instructions
│── IDS.py                   # IDS and ML classification scripts for testing dataset
│── RPL-IDS-Beh.csv          # Complete processed dataset for IDS evaluation
│── .gitignore               # List of files/folders to be ignored by Git

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
./gradlew run
```

---

## 🚀 Running the Simulation to Verify Correctness

- Open Cooja and navigate to `contiki-ng\IDS-example\Visualization\dataset`
- Open the provided `.csc` simulation files
- Click **Start** to begin the network simulation
- The modified nodes should generate log files containing network behavior
- Verify that the log files are being generated correctly and contain entries with "ids:"
- If everything is correct, close Cooja
- Open a terminal and navigate to dataset directory
```
cd contiki-ng\IDS-example\Visualization\dataset
```
- Run `sequential_executor.py` to execute multiple network simulations in no-GUI mode.
```
    python3 sequential_executor.py
```
sequential_executor.py will automatically run all .csc Cooja simulation files in the current directory using no-GUI mode.
This process will generate the required log files for further analysis.


### 🔹 Network Simulation Files
Before running `sequential_executor.py`, ensure that there are **six `.csc` network simulation files** in the `dataset` directory.  
These files represent different network scenarios with **varying numbers of nodes and root positions**.

Researchers can also **test other network configurations** by placing their own `.csc` files in the same `dataset` directory.  
Any additional `.csc` files placed in this directory will be automatically executed during the simulation process.


### 🔹 Attack Configuration
This execution will use the attack parameters defined in project-conf.h file in the path:
/contiki-ng/LSM-example/Visualization/IDS/project-conf.h

To activate or deactivate specific attack types, edit the following parameters in `project-conf.h`:
```c
#define CONF_SFA 0 //  Selective Forward Attack
#define CONF_VNA 1 //  Version Number Attack
#define CONF_DRA 1 //  Decrease Rank Attack
#define CONF_IRA 0 //  Increase Rank Attack
```
However, all attack combinations are already pre-configured and executed.
The generated log files **can be found** in the sub-folders of the dataset folder.


# 📊 Dataset Generation & IDS Testing

Once simulation logs are collected, use Python scripts for dataset processing and IDS evaluation.  
These steps **do not require** COOJA Simulator or an Ubuntu environment and can be executed on **Windows** using Python.
To do this, download the `python-analysis` folder from the repository to your Windows OS.

## **1️⃣ Process Simulation Logs**
Ensure that the log files for any attack scenario are placed inside the `dataset` folder under:

\python-analysis\dataset

Then, run the dataset generation script to create the dataset file `RPL-IDS-Beh.csv`:
```
cd \python-analysis 
python3 dataset_generation.py
```


## **2️⃣ Run IDS Evaluation**
Test the **Intrusion Detection System (IDS)** using machine learning models:
```
python IDS.py
```
Running `IDS.py` will output multiple evaluation metrics, including:
- **Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **Confusion Matrix** (showing the classification results for different attack types)


## **3️⃣ Analyze Feature Importance**
To understand which features contribute most to attack detection:
```
cd \feature_importance 
python3 feature_importance.py
```

The `feature_importance.py` script will generate an image with a bar graph representing the **top 10 most important features**.

### ✅ Notes:
- Ensure **Python** is installed on your Windows OS.
- Place the correct log files in the `dataset` folder before running `dataset_generation.py`.
- The generated dataset file `RPL-IDS-Beh.csv` will be used for IDS evaluation and feature analysis.



---

## 📄 Dataset Description
The dataset contains:
- **Node-specific features** (e.g., RPL rank, version number, packet counts).
- **Neighbor-aggregated features** (e.g., average forwarded packets).
- **Derived features** (e.g., rank difference, control-to-data packet ratio).


---

## 📜 License
This project is released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 📬 Contact & Contributions
- **Author:** HUNSR  
- **GitHub Issues:** [Submit a Bug Report](https://github.com/HUNSR/RPL-IDS-Behavior-Dataset/issues)  
- **Pull Requests:** Contributions are welcome! Feel free to open a PR.

---

