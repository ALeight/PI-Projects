**Overview** 
A simple integration project programmed on a Raspberry PI 5 
as a sort of inauguration. The project includes an API call, including encoding of the JSON response. This response is used to plot the data onto a chart, using Pythons matplotlib. 

### Setup 
1. Create a .env file:
    ```
    EMAIL_USER=what@ever.com
    EMAIL_RECIPIENT=reci@eve.com
    ```
2. Store your Gmail App Password securely: 
    ```bash
    python -c "import keyring; keyring.set_password('email_service', 'your@email.com', 'your_app_password')
    ```
3. Run the script: 
    ```bash
    python3 weatherReport.py
    ```

### Email Delivery
Emails are sent via Gmail using STMP with SSL (port 465). Make sure to generate an [App Password](ttps://myaccount.google.com/apppasswords). 