@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reality Check AI</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                background: url('/static/background.png') no-repeat center center fixed;
                background-size: cover;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-family: 'Poppins', sans-serif;
                color: #fff;
                text-align: center;
                backdrop-filter: blur(6px);
            }
            .glass {
                background: rgba(0, 0, 0, 0.6);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 0 25px rgba(0,0,0,0.4);
                max-width: 400px;
                width: 90%;
            }
            img {
                width: 120px;
                margin-bottom: 20px;
                border-radius: 50%;
                border: 2px solid rgba(255,255,255,0.3);
            }
            h1 {
                font-size: 1.8em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1em;
                opacity: 0.8;
                margin-bottom: 20px;
            }
            input[type=file] {
                margin: 10px 0;
            }
            button {
                background: linear-gradient(90deg, #00b4d8, #0077b6);
                border: none;
                padding: 10px 20px;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                transition: 0.3s;
            }
            button:hover {
                background: linear-gradient(90deg, #0077b6, #00b4d8);
            }
        </style>
    </head>
    <body>
        <div class="glass">
            <img src="/static/logo.png" alt="Reality Check Logo">
            <h1>Reality Check AI</h1>
            <p>Upload any image or video to verify if it's real or AI-generated.</p>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*,video/*" required>
                <br>
                <button type="submit">Analyze</button>
            </form>
        </div>
    </body>
    </html>
    '''
