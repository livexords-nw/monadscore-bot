---

<h1 align="center">Monadscore Bot</h1>

<p align="center">Automate tasks in Monadscore to boost your efficiency and maximize rewards! 🚀</p>

---

## 🚀 About the Bot

**Monadscore Bot** is designed to automate various tasks on **Monadscore**, helping you to:

- **📝 Auto Solve Task:** Automatically solve tasks and claim rewards.
- **⚙️ Auto Run Node:** Execute and monitor nodes without manual intervention.
- **🔗 Auto Reff:** Generate referral accounts effortlessly.
- **🌐 Support Proxy:** Dynamically assign proxies for each account.
- **👥 Support Multi Account:** Manage multiple accounts at the same time.
- **🧵 Support Thread:** Process multiple accounts concurrently with adjustable threading.
- **⏱️ Delay Loop & Account Switching:** Customize delay intervals for looping and switching accounts to optimize performance.

---

## 🌟 Version v1.0.1

### What's New

- Adjusted all API endpoints to align with the updated monadscore API

---

## ⚙️ Main Configuration (`config.json`)

```json
{
  "task": true,
  "run_account_reff": true,
  "thread": 1,
  "proxy": false,
  "delay_account_switch": 10,
  "delay_loop": 43200
}
```

| **Parameter**          | **Description**                                       | **Default** |
| ---------------------- | ----------------------------------------------------- | ----------- |
| `task`                 | Automate task solving and reward claims 🔍            | `true`      |
| `run_account_reff`     | Enable referral account generation 🔗                 | `false`      |
| `thread`               | Number of concurrent threads (accounts) to process 🧵 | `1`         |
| `proxy`                | Enable/Disable proxy usage 🌐                         | `false`     |
| `delay_account_switch` | Delay between account switches (in seconds) ⏱️        | `10`        |
| `delay_loop`           | Delay before the next loop iteration (in seconds) ⏲️  | `43200`     |

---

### Referral Configuration (`config_reff.json`)

```json
{
  "proxy": true,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

| **Parameter**          | **Description**                                                           | **Default** |
| ---------------------- | ------------------------------------------------------------------------- | ----------- |
| `thread`               | Number of concurrent threads (accounts) to process 🧵 | `1`         |
| `proxy`                | Enable/Disable proxy usage for referral generation 🌐                     | `true`      |
| `delay_account_switch` | Delay between account switches during referral generation (in seconds) ⏱️ | `10`        |
| `delay_loop`           | Delay before the next referral loop iteration (in seconds) ⏲️        | `3000`      |

---

## 📥 How to Register

Get started with Monadscore Bot by registering through the link below:

<div align="center">
  <a href="https://monadscore.xyz/signup/r/JioRgBeR" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Monadscore&logo=telegram&label=&color=2CA5E0&logoColor=white&style=for-the-badge" height="25" alt="Telegram Logo" />
  </a>
</div>

---

## 📖 Installation Steps

### General Installation

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/monadscore-bot.git
   ```

   > 💡 _Tip: Ensure you have Git installed on your machine!_

2. **Navigate to the Project Folder**  
   Move into the project directory:

   ```bash
   cd monadscore-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

   > ✅ _All dependencies will be installed automatically!_

4. **Configure Query**  
   Create a `query.txt` file and add your Monadscore query data.  
   **Example content (each line is a wallet address):**

   ```
   0x10f57C949bb75DFDb04278EA04baDC85CB2e0Bda
   0x10f57C949bb75DFDb04278EA04baDC85CB2e0Bda
   0x10f57C949bb75DFDb04278EA04baDC85CB2e0Bda
   ```

   > 💡 _Tip: You can include multiple wallet addresses by adding each on a new line._

5. **Set Up Proxy (Optional)**  
   If you wish to use a proxy, create a `proxy.txt` file and add your proxies in the following format:

   ```
   http://username:password@ip:port
   ```

   > 🌐 _Only HTTP and HTTPS proxies are supported._

6. **Run the Bot**  
   Launch the bot with the following command:
   ```bash
   python main.py
   ```
   > 🚀 _Your bot will start running and automating tasks!_

---

### Referral Installation Tutorial

1. **Install Dependencies**  
   Make sure you’ve installed the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create Referral File**  
   Create a file named `query_reff.txt` in the project directory. Populate the file with your referral links and generation counts.  
   **Example content:**

   ```
   https://monadscore.xyz/signup/r/JioRgBeR|5
   https://monadscore.xyz/signup/r/JioRgBeR|5
   https://monadscore.xyz/signup/r/JioRgBeR|5
   ```

   > 💡 _Tip: You can add as many lines as needed. Successful referral wallet addresses will be stored in `result_reff.txt` automatically._

3. **Run the Referral Module**  
   Start the referral module by running:
   ```bash
   python reff.py
   ```
   > 🚀 _Your referral generation process will begin immediately!_

---

## 🤝 Contributing

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, please reach out:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&style=for-the-badge" height="25" alt="Telegram Logo" />
  </a>
</div>

---
