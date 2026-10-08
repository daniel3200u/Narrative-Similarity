# DPO Training with TRL and Modal

Project untuk melakukan fine-tuning Large Language Model (LLM) menggunakan **Direct Preference Optimization (DPO)** dengan **Hugging Face TRL**, **PEFT/LoRA**, dan **Modal GPU**.

## Project Structure

```text
dpo-project/
│
├── data/
│   ├── train.jsonl
│   └── eval.jsonl
│
├── src/
│   ├── train.py
│   └── inference.py
│
├── modal_app.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.10+
* Hugging Face Transformers
* Hugging Face TRL
* PEFT
* Datasets
* Modal
* GPU untuk training

Training GPU dijalankan menggunakan Modal sehingga GPU tidak harus tersedia di komputer lokal.

## Installation

Clone project:

```bash
git clone <URL_REPOSITORY>
cd dpo-project
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Modal Setup

Install Modal:

```bash
pip install modal
```

Login ke Modal:

```bash
modal setup
```

Setelah login, project dapat menjalankan training GPU melalui Modal.

## Dataset

Dataset DPO terdiri dari tiga bagian:

```text
prompt
chosen
rejected
```

Contoh `data/train.jsonl`:

```json
{"prompt":"Apa itu Python?","chosen":"Python adalah bahasa pemrograman tingkat tinggi yang mudah digunakan dan banyak digunakan dalam pengembangan software, data science, dan AI.","rejected":"Python adalah sebuah komputer."}
{"prompt":"Apa itu machine learning?","chosen":"Machine learning adalah metode yang memungkinkan komputer mempelajari pola dari data untuk membuat prediksi atau keputusan.","rejected":"Machine learning adalah cara memperbaiki komputer."}
```

### Penjelasan

`prompt` adalah input atau pertanyaan.

`chosen` adalah jawaban yang dianggap lebih baik.

`rejected` adalah jawaban yang dianggap lebih buruk.

DPO menggunakan pasangan `chosen` dan `rejected` untuk mempelajari preferensi.

## Training

Training dapat dijalankan melalui Modal:

```bash
modal run modal_app.py
```

Modal akan menjalankan proses training pada GPU cloud.

Secara umum workflow-nya:

```text
Dataset
   ↓
Base Model
   ↓
DPOTrainer
   ↓
LoRA Adapter
   ↓
Fine-tuned Model
```

## Model

Model yang digunakan dapat diubah pada konfigurasi training.

Contoh:

```python
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
```

Model yang lebih besar membutuhkan resource GPU yang lebih besar.

## LoRA

Training menggunakan LoRA agar parameter yang perlu dilatih lebih sedikit dibandingkan full fine-tuning.

Contoh konfigurasi:

```python
LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM",
)
```

## Output

Hasil training disimpan pada folder output:

```text
outputs/
└── dpo-model/
```

Jika menggunakan LoRA, output utama berupa adapter yang dapat digunakan bersama base model.

## Inference

Setelah training selesai, adapter dapat digunakan untuk inference menggunakan script:

```bash
python src/inference.py
```

Workflow inference:

```text
Base Model
     +
LoRA Adapter
     ↓
Fine-tuned Model
     ↓
Generate Response
```

## Development Workflow

Project dikembangkan menggunakan VS Code.

Workflow:

```text
VS Code
   │
   ├── Edit Python
   ├── Edit Dataset
   └── Edit Configuration
          │
          ▼
     modal run
          │
          ▼
      Modal Cloud
          │
          ▼
        GPU
          │
          ▼
     DPO Training
```

## Useful Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Login Modal:

```bash
modal setup
```

Run training:

```bash
modal run modal_app.py
```

Run inference:

```bash
python src/inference.py
```

## Notes

Pastikan dataset memiliki format DPO yang benar:

```text
prompt → chosen / rejected
```

Gunakan `chosen` untuk response yang lebih baik dan `rejected` untuk response yang ingin dikurangi probabilitasnya oleh model.

## License

MIT
