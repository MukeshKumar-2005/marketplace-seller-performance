\# Marketplace Seller Performance Analytics



\## Project Overview



A Python-based data engineering project that processes marketplace data through an ETL pipeline, stores it in MySQL, and provides seller and product performance analytics through FastAPI.



\## Features



\- Automated ETL pipeline using Python and Pandas.

\- Data cleaning and transformation.

\- MySQL database integration.

\- Seller performance analysis.

\- Category-wise and monthly revenue analysis.

\- Product sales analytics.

\- REST API development using FastAPI.

\- Automated API testing using Pytest.



\## Technologies Used



| Technology | Purpose |

|---|---|

| Python | Core programming |

| Pandas | Data processing |

| NumPy | Numerical operations |

| MySQL | Database |

| SQL | Data analytics |

| FastAPI | REST API development |

| Uvicorn | API server |

| Pytest | Automated testing |

| Git | Version control |



\## Project Structure



```text

marketplace-seller-performance/

│

├── api/

│   ├── main.py

│   ├── routes/

│   │   └── analytics.py

│   └── schemas/

│       └── analytics.py

│

├── data/

│   ├── input/

│   ├── internal/

│   ├── raw/

│   └── processed/

│

├── etl/

│   ├── extract.py

│   ├── transform.py

│   └── load.py

│

├── scripts/

│   └── generate\_data.py

│

├── tests/

│   └── test\_api.py

│

├── db\_connection.py

├── create\_tables.py

├── requirements.txt

├── .env.example

└── README.md

```



\## ETL Pipeline



The project follows three stages:



\### 1. Extract

Reads marketplace data from CSV files.



\### 2. Transform

Cleans, processes, and prepares data using Pandas.



\### 3. Load

Loads processed data into MySQL and calculates seller performance metrics.



\## Database



Database: `performance\_db`



Main tables:



\- sellers

\- products

\- orders

\- order\_items

\- payments

\- seller\_performance



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET | `/` | API home |

| GET | `/api/health` | Health check |

| GET | `/api/analytics/top-sellers` | Top five sellers |

| GET | `/api/analytics/category-revenue` | Category revenue |

| GET | `/api/analytics/monthly-revenue` | Monthly revenue |

| GET | `/api/analytics/average-order-value` | Average order value |

| GET | `/api/analytics/best-products` | Best-selling products |

| GET | `/api/analytics/seller-ranking` | Seller revenue ranking |



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd marketplace-seller-performance

```



\### 2. Create and activate a virtual environment



```bash

python -m venv venv

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file using `.env.example` as a template.



Add your own local MySQL credentials. Never commit the actual `.env` file.



\### 5. Create database tables



```bash

python create\_tables.py

```



\### 6. Generate sample data



```bash

python scripts/generate\_data.py

```



\### 7. Execute the ETL pipeline



```bash

python etl/extract.py

python etl/transform.py

python etl/load.py

```



\### 8. Start the API server



```bash

uvicorn api.main:app --reload

```



Open the API documentation:



http://127.0.0.1:8000/docs



\## Running Tests



Execute:



```bash

python -m pytest tests/test\_api.py -v

```



Latest verified result: \*\*8 tests passed\*\*.



\## Sample Dataset



The generated sample dataset contains:



\- 20 sellers

\- 100 products

\- 500 orders

\- 1,285 order items



\## Future Improvements



\- Database-mocking unit tests.

\- Logging and improved error handling.

\- Docker integration.

\- Cloud deployment.

\- Interactive analytics dashboard.
