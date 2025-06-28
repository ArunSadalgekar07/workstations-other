# AccessGrid GPU Monitoring & User Management Dashboard

A Flask-based web dashboard for monitoring GPU and CPU stats across multiple department servers, managing users, and analyzing GPU usage from CSV files.

---

## 🚀 Features

- **Multi-Server GPU Monitoring** - Monitor GPUs across multiple department workstations
- **Live GPU & CPU Monitoring** (Linux)
- **User Management** (create, delete, list, search, inactive users)
- **CSV Analysis**: Upload and visualize GPU usage data
- **Historical Data Analysis** - View GPU usage trends over time
- **Downloadable Reports** (charts, inactive users, CSV logs)
- **Modern, Responsive UI** with loading indicators and interactive charts
- **Server Status Dashboard** - Overview of all department servers

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Environment Setup**
Create a `.env` file with your admin credentials:
```env
ACCESSGRID_ADMIN_USER=admin
ACCESSGRID_ADMIN_PASS=admin
```

### 4. **Run the App**
```bash
python app.py
```
- The app will be available at [http://localhost:5000](http://localhost:5000)

### 5. **Login**
- Default credentials:  
  **Username:** `admin`  
  **Password:** `admin`

---

## 📂 Folder Structure

```
.
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── gpu_logger.sh                   # GPU logging script
├── gpu_logger.py                   # Python GPU logger
├── utils/
│   ├── db.py                      # Database operations
│   └── shell_ops.py               # Shell operations for user management
├── static/
│   ├── images/                    # UI images and logos
│   └── *.css                      # Stylesheets
├── templates/
│   ├── dashboard.html             # Main dashboard
│   ├── login.html                 # Login page
│   ├── display.html               # Display page
│   ├── serverdashboard.html       # Server dashboard
│   ├── user_utilization.html      # User utilization page
│   ├── csv_analysis.html          # CSV analysis page
│   ├── status.html                # GPU status page
│   └── ... (other HTML templates)
└── GPU_Usage_Logs/                # GPU usage log files
```

---

## 🧑‍💻 Usage Examples

- **Monitor live GPU/CPU stats** across all department servers
- **View server status** and GPU availability
- **Upload a CSV** on the CSV Analysis page to visualize GPU usage
- **Manage users** (create, delete, list, search, view inactive)
- **Download** charts, inactive user lists, and CSV logs as files
- **Track historical GPU usage** with time-based filtering

---

## 📝 API Documentation

### **Authentication**
- Most API endpoints require a valid session (login via web UI)
- Some endpoints are publicly accessible for server status

---

### **Web Routes**

#### `GET /`
- **Description:** Root route - redirects to login page
- **Auth:** None
- **Redirects:** `/login`

#### `GET /login`
- **Description:** Login page
- **Auth:** None
- **Methods:** GET, POST

#### `GET /dashboard`
- **Description:** Main dashboard page
- **Auth:** Session required

#### `GET /display`
- **Description:** Display page
- **Auth:** Session required

#### `GET /server_dashboard`
- **Description:** Server utilization dashboard
- **Auth:** Session required

#### `GET /user_utilization`
- **Description:** User utilization page
- **Auth:** Session required

#### `GET /search_user`
- **Description:** Search users page
- **Auth:** Session required
- **Methods:** GET, POST

#### `GET /create_user`
- **Description:** Create user form
- **Auth:** Session required
- **Methods:** GET, POST

#### `GET /delete_user`
- **Description:** Delete user form
- **Auth:** Session required
- **Methods:** GET, POST

#### `GET /list_users`
- **Description:** List all users
- **Auth:** Session required

#### `GET /inactive_users`
- **Description:** Show inactive users (30+ days)
- **Auth:** Session required

#### `GET /csv_analysis`
- **Description:** CSV analysis page
- **Auth:** None

#### `GET /status`
- **Description:** GPU status page
- **Auth:** None

#### `GET /download_csvs`
- **Description:** Download CSV logs page
- **Auth:** Session required

#### `GET /download_csv/<filename>`
- **Description:** Download specific CSV file
- **Auth:** Session required

#### `GET /logout`
- **Description:** Logout and clear session
- **Auth:** None
- **Redirects:** `/login`

---

### **API Endpoints**

#### `GET /api/gpu_stats`
- **Description:** Get live GPU stats
- **Auth:** None (commented out)
- **Response:**  
  ```json
  [
    {
      "index": 0,
      "name": "NVIDIA RTX 6000 Ada Generation",
      "gpu_util": 2,
      "mem_util": 413,
      "mem_total": 49140,
      "mem_used": 413,
      "mem_free": 48727,
      "temperature": 45
    }
  ]
  ```

#### `GET /api/cpu_live_info`
- **Description:** Get live CPU info (Linux only)
- **Auth:** None
- **Response:**  
  ```json
  {
    "cpu_percent": 12.5,
    "per_core": [10.0, 15.0, ...],
    "load_avg": [0.5, 0.7, 0.8],
    "model_name": "Intel(R) Xeon(R) CPU"
  }
  ```

#### `GET /api/user_gpu_usage`
- **Description:** Get current user GPU usage
- **Auth:** None (commented out)
- **Response:**  
  ```json
  [
    {
      "username": "user1",
      "gpu_memory_mib": 2048
    }
  ]
  ```

#### `POST /api/analyze_csv`
- **Description:** Analyze uploaded GPU CSV file
- **Auth:** None
- **Body:** `multipart/form-data` with `csvFile`
- **Response:**  
  ```json
  [
    {
      "index": 0,
      "name": "NVIDIA RTX 6000 Ada Generation",
      "timestamps": ["2025-04-29 14:18:23", ...],
      "utilization": [2, ...],
      "memory": [413, ...]
    }
  ]
  ```

#### `GET /api/historical_gpu_stats`
- **Description:** Get historical GPU stats
- **Auth:** Session required
- **Query Parameters:**
  - `range`: daily, weekly, monthly
  - `start_date`: Custom start date (YYYY-MM-DD)
  - `end_date`: Custom end date (YYYY-MM-DD)
- **Response:** Same as `/api/gpu_stats` with historical data

#### `GET /api/historical_user_gpu_usage`
- **Description:** Get historical user GPU usage
- **Auth:** Session required
- **Query Parameters:**
  - `range`: daily, weekly, monthly
- **Response:**  
  ```json
  [
    {
      "username": "user1",
      "timestamps": ["2025-04-29 14:18:23", ...],
      "gpu_memory_mib": [2048, ...],
      "gpu_memory_percentage": [4.2, ...]
    }
  ]
  ```

#### `GET /api/gpu_status`
- **Description:** Check GPU status for server list page
- **Auth:** None
- **Response:**  
  ```json
  {
    "status": "working",
    "gpu_count": 3,
    "working_gpus": 3,
    "gpu_details": [...]
  }
  ```

#### `GET /api/all_gpu_status`
- **Description:** Get GPU status from all department workstations
- **Auth:** None
- **Response:**  
  ```json
  [
    {
      "name": "CS-1",
      "gpus": [
        {"status": "green", "gpu": {...}},
        {"status": "red", "gpu": null}
      ],
      "reachable": true
    }
  ]
  ```

---

## 🔧 Configuration

### **Workstation Configuration**
The application monitors these department workstations:
- CS-1: `http://172.0.16.27:5000`
- CS-2: `http://172.0.16.29:5000`
- MECH: `http://172.0.16.26:5000`
- EC: `http://172.0.16.25:5000`
- CIVIL: `http://172.0.16.28:5000`
- ASUS: `http://172.0.16.31:5000`

### **GPU Logging**
- GPU usage is logged every 5 seconds by default
- Logs are stored in `GPU_Usage_Logs/` directory
- Files are organized by daily, weekly, and monthly periods

---

## 🔒 Security Notes

- Change the default admin password after setup
- For production, use HTTPS and secure session management
- Consider implementing rate limiting for API endpoints
- Review and secure the workstation IP addresses

---

## 🧩 Contributing

Pull requests and suggestions are welcome!

---

## 📊 Monitoring Features

- **Real-time GPU monitoring** across multiple servers
- **User activity tracking** and utilization analysis
- **Historical data analysis** with customizable time ranges
- **CSV data import** for external GPU usage analysis
- **Automated logging** of GPU usage patterns


