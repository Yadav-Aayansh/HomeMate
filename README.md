# HomeMate
A multi-user platform offering comprehensive household services, connecting customers with verified service professionals, managed by an admin using robust backend operations and role-based access control.

## 🚀 Preview
[![Watch the video](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate13.png)](https://youtu.be/uhcoqsnWUHc?si=kB4CqK7C0WLHVuGh)

<h3 align="center">
  Demo URL (Please, Open in Desktop):
  <br>
  Coming Soon...
</h3>

## 💻 Built with

### Backend
- **Flask**: A web framework.
- **Flask_SQLAlchemy**: Manages database operations.
- **Flask-JWT-Extended**: For handling JSON Web Tokens.
- **Flask_RESTful**: Simplifies creating REST APIs.
- **Flask-Caching**: Adds caching support.
- **Celery**: Handles asynchronous tasks.
- **Redis**: Message broker and caching layer.
- **WeasyPrint**: Generates PDFs and prints HTML to documents.
- **Razorpay**: Integrates payment gateway.

### Database
- **SQLite**: A lightweight database.

### Frontend
- **HTML**: For structuring web pages.
- **CSS**: Styles web pages.
- **JavaScript**: Adds interactivity.
- **VueJS**: Builds dynamic, reactive user interfaces.
- **Vite**: Provides fast development environment for VueJS.
- **Bootstrap**: For responsive and mobile-first design.
- **ChartJS**: Visualizes data through charts.

## ⚙️ Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Yadav-Aayansh/HomeMate.git
```

### 2. Change the working directory
```bash
cd HomeMate
```

### 3. Setup Backend (Server)

#### a. Create a Virtual Environment
```bash
cd server
python -m venv venv
```

#### b. Install Required Backend Package Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Frontend (Client)

#### a. Install Frontend Dependencies
```bash
cd ../client
npm install
```

### 5. Setup Redis
Make sure Redis is installed and running. You can start Redis using:
```bash
redis-server
```

### 6. Run Celery Worker
In a new terminal window, run the Celery worker:
```bash
cd ../server
celery -A app.celery worker --loglevel=info
```

### 7. Run Celery Beat
In another terminal window, run the Celery Beat scheduler:
```bash
cd ../server
celery -A app.celery beat --loglevel=info
```

### 8. Run the Backend
In the main terminal, run the Flask app:
```bash
cd ../server
python run.py
```

### 9. Run the Frontend Development Server
In the client directory, run the Vite server:
```bash
cd ../client
npm run dev
```

🌟 You are all set!
<hr>

## 📸 Screenshots
![Admin Dashboard](https://github.com/user-attachments/assets/a15c6960-b2fc-47ee-b955-8bd140becf6d)
![Admin Dashboard](https://github.com/user-attachments/assets/21741f0c-46c6-4e6e-b8bb-8a74408aed1f)
![Admin Dashboard](https://github.com/user-attachments/assets/a498c27b-9a01-4861-8d19-7cdf1a3a9339)
![Influencer Dashboard](https://github.com/user-attachments/assets/117bf2d7-8110-455b-8c6c-b204eebe9803)
![Influencer Dashboard](https://github.com/user-attachments/assets/7b15a81f-67c6-4174-8b91-aaa17d912766)
![Sponsor Dashboard](https://github.com/user-attachments/assets/ba875261-2679-480c-8fc8-76b36164b357)
![Sponsor Dashboard](https://github.com/user-attachments/assets/15b43391-7ffc-4e96-a7a3-8544a9d80ebc)
![Sponsor Dashboard](https://github.com/user-attachments/assets/f3df72ad-d586-4c92-ba4e-be166ccd23e8)

<hr>
<h3 align="center">
Thank You ❤️
</h3>
