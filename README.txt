Nassau Candy Distributor — Decision Intelligence Project
=========================================================

DELIVERABLES
------------
1. Nassau_Candy_Research_Paper.docx  — Full 21-page research paper
2. Nassau_Candy_Executive_Summary.docx — 1-page stakeholder summary
3. Dashboard/ — Streamlit web application (live analytics)
4. Data and Outputs/ — Raw data, clustering outputs, findings

HOW TO RUN THE DASHBOARD
--------------------------
1. Open Google Colab (colab.research.google.com)
2. Upload all files from the Dashboard/ folder
3. Run the following commands in a cell:

   !pip install streamlit pyngrok -q
   from pyngrok import ngrok
   ngrok.set_auth_token("YOUR_NGROK_TOKEN")

   import time
   get_ipython().system_raw('streamlit run app.py --server.port 8501 &')
   time.sleep(6)
   print(ngrok.connect(8501))

4. Click the link that appears — the dashboard will open in your browser

TOOLS USED
-----------
Python, Pandas, Scikit-learn, Streamlit, Google Colab