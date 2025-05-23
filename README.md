# HomeMate
A multi-user platform offering comprehensive household services, connecting customers with verified service professionals, managed by an admin using robust backend operations and role-based access control.

## 🚀 Preview
[![Watch the video](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate13.png)](https://youtu.be/uhcoqsnWUHc?si=kB4CqK7C0WLHVuGh)

<h3 align="center">
  Demo URL (Please, Open in Desktop):
  <br>
  <a href="https://the-homemate.vercel.app" target="_blank"> the-homemate.vercel.app </a>
</h3>

<div align="center">

<h3><strong>Test Users</strong></h3>

<table>
  <thead>
    <tr>
      <th align="left">Role</th>
      <th align="left">Username</th>
      <th align="left">Password</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Admin</strong></td>
      <td><code>Noctivagous</code></td>
      <td><code>12345678</code></td>
    </tr>
    <tr>
      <td><strong>Customer</strong></td>
      <td><code>Billy_Butcher</code></td>
      <td><code>12345678</code></td>
    </tr>
    <tr>
      <td><strong>Professional</strong></td>
      <td><code>Aayansh</code></td>
      <td><code>12345678</code></td>
    </tr>
  </tbody>
</table>

</div>



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

### 3. Create & Activate Virtual Environment
- #### Create Virtual Environment
  
```bash
cd server
python -m venv venv
```

- #### Activate Virtual Environment
For Linux/macOS:
```
source venv/bin/activate
```
For Windows:
```
venv\\Scripts\\activate
```

### 4. Install Required Backend Package Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Backend
```bash
python run.py
```

### 6. Install Frontend Dependencies
In a new terminal window, install frontend dependencies:
```bash
cd ../client
npm install
```

### 7. Run the Frontend Development Server
```bash
npm run dev
```

### 8. Setup Redis
Make sure Redis is installed and running. You can start Redis using:
```bash
redis-server
```

### 9. Run Celery Worker
In a new terminal window, run the Celery worker:
```bash
cd ../server
celery -A run.celery worker --loglevel=info
```

### 10. Run Celery Beat
In another terminal window, run the Celery Beat scheduler:
```bash
celery -A run.celery beat --loglevel=info
```

🌟 You are all set!
<hr>

## 📸 Screenshots
![HomeMate1](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate1.png)
![HomeMate2](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate2.png)
![HomeMate3](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate3.png)
![HomeMate4](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate4.png)
![HomeMate5](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate5.png)
![HomeMate6](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate6.png)
![HomeMate7](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate7.png)
![HomeMate8](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate8.png)
![HomeMate9](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate9.png)
![HomeMate10](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate10.png)
![HomeMate11](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate11.png)
![HomeMate12](https://github.com/Yadav-Aayansh/Assets/blob/main/HomeMate12.png)

<hr>
<h3 align="center">
Thank You 🫡
</h3>
