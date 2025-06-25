"""
Gas Guard Optimizer
Оптимизатор комиссии газа Ethereum на основе анализа последних данных сети.
"""

import requests
import datetime
import time
import matplotlib.pyplot as plt

ETH_GAS_API = "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"

def fetch_gas_data():
    try:
        res = requests.get(ETH_GAS_API)
        data = res.json()["result"]
        return {
            "SafeGasPrice": int(data["SafeGasPrice"]),
            "ProposeGasPrice": int(data["ProposeGasPrice"]),
            "FastGasPrice": int(data["FastGasPrice"]),
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print("Ошибка при получении данных о газе:", e)
        return None

def monitor(interval=60, duration=3600):
    print("⛽ Старт мониторинга сети Ethereum...")
    gas_history = []
    start_time = time.time()

    while time.time() - start_time < duration:
        data = fetch_gas_data()
        if data:
            gas_history.append(data)
            print(f"[{data['timestamp']}] Safe: {data['SafeGasPrice']} | Propose: {data['ProposeGasPrice']} | Fast: {data['FastGasPrice']}")
        time.sleep(interval)

    return gas_history

def visualize_gas_history(gas_history):
    times = [entry["timestamp"] for entry in gas_history]
    safe = [entry["SafeGasPrice"] for entry in gas_history]
    propose = [entry["ProposeGasPrice"] for entry in gas_history]
    fast = [entry["FastGasPrice"] for entry in gas_history]

    plt.figure(figsize=(12, 6))
    plt.plot(times, safe, label="Safe", color="green")
    plt.plot(times, propose, label="Propose", color="orange")
    plt.plot(times, fast, label="Fast", color="red")
    plt.xticks(rotation=45)
    plt.ylabel("Gas Price (Gwei)")
    plt.title("История изменения цены газа Ethereum")
    plt.legend()
    plt.tight_layout()
    plt.savefig("gas_price_history.png")
    plt.show()

if __name__ == "__main__":
    history = monitor(interval=60, duration=600)  # 10 минут сбора данных
    visualize_gas_history(history)
