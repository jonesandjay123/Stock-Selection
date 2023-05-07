# My Nasdaq Data Link Project

這個專案使用了 Nasdaq Data Link 的 Python 客戶端來獲取金融數據。

## 環境設置

1. 安裝[Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/distribution)，以便使用`conda`命令。

2. 創建一個新的 conda 環境，並安裝所需的 Python 版本（例如，3.10）：

   ```shell
   conda create --name nasdaq_env python=3.10
   ```

3. 啟動新創建的 conda 環境：

   - 對於 macOS 和 Linux：

   ```shell
   conda activate nasdaq_env

   ```

4. 安裝所需的套件：

   ```shell
   conda install -c conda-forge nasdaq-data-link pandas
   ```

   如果 nasdaq-data-link 在 conda-forge 通道中無法找到，您可以改用 pip 來安裝：

   ```shell
   pip install -r requirements.txt
   ```

5. 運行您的 Python 腳本。

6. 完成後，退出 conda 環境：

   對於 macOS 和 Linux：

   ```shell
   conda deactivate
   ```

to pack into exe file:
```shell
pyinstaller --onefile --noconsole --additional-hooks-dir=hooks daily_stock_select.py
```